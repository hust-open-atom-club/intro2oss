# Docker Compose 实践

!!! note "主要作者"

    CAICAII

## 从单容器到容器编排

在前面的课程中，我们学习了如何使用 Docker 容器来运行单个服务。
通过 `docker run` 命令，我们可以快速启动一个数据库、一个 Web 服务器或者一个缓存服务。
这种方式在开发简单应用时非常有效。然而，随着应用架构的演进，微服务的理念逐渐流行，一个应用可能由多个相互依赖的服务组成。
如果继续使用单容器管理方式，我们需要手动管理容器间的网络连接、存储卷映射、环境变量配置等，这不仅增加了运维的复杂度，还容易因手动操作而出错。

这就是为什么我们需要一个更高层次的工具来管理多容器应用。
Docker Compose 应运而生，它通过一个声明式的 YAML 配置文件，帮助我们定义和管理多容器应用。
通过 Docker Compose，我们可以用一个命令就完成整个应用的部署，而不需要手动管理每个容器。

## Docker Compose 核心概念

Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。使用 Compose，你可以通过一个 YAML 文件来配置应用程序的所有服务，然后使用一个命令来创建和启动所有服务。

### 主要概念

- **服务 (Services)**：容器的定义，包括使用哪个镜像、端口映射、环境变量等
- **网络 (Networks)**：定义容器之间如何通信
- **卷 (Volumes)**：定义数据的持久化存储
- **依赖关系 (Dependencies)**：定义服务之间的启动顺序
- **环境变量 (Environment Variables)**：管理不同环境的配置

### 核心命令

- `docker compose up`：创建和启动所有服务
- `docker compose down`：停止和删除所有服务
- `docker compose ps`：查看服务状态
- `docker compose logs`：查看服务日志

## 实践项目：使用 docker compose 构建 Todo 应用

在本章节中，我们通过一个最小可用的 Todo 应用来实战 Docker Compose 编排。示例使用官方镜像，其中后端采用真实工程结构（源码 + Dockerfile），前端与 Nginx 为了演示方便用容器内命令动态生成配置。

### 目标组件

- **Nginx**：统一入口与反向代理 (对外 8080)
- **前端**：CDN 版 React 静态页，由 Nginx 托管
- **后端**：Node.js Express API (容器内 3001)，由 `backend/Dockerfile` 构建
- **数据库**：MongoDB (容器内 27017)

### 项目结构 (示意)

```text
compose-demo/
├── compose.yaml          # Compose 配置
└── backend/
    ├── Dockerfile        # 后端的构建文件
    ├── package.json      # 后端依赖清单
    └── server.js         # 后端源码
```

### 架构图

```text
                        ┌─────────────┐
                        │   Nginx     │
                        │   :8080     │
                        └─────┬───────┘
                             │
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼─────┐   ┌──────▼──────┐
            │  Frontend   │   │   Backend    │
            │  (React)    │   │  (Node.js)   │
            │   :80       │   │    :3001     │
            └─────────────┘   └──────┬───────┘
                                    │
                            ┌───────▼───────┐
                            │   MongoDB     │
                            │  Database     │
                            │    :27017     │
                            └───────────────┘
```

### Docker Compose 配置

将下列 `compose.yaml` 内容复制到你的工程中使用。

!!! note "为什么不再写 `version: \"3.9\"`"

    Compose 文件顶层的 `version:` 字段来自早期的 Compose file format 规范。现在通用的
    **Compose Spec** 已经把它废弃：写了它只会让 `docker compose` 打印 deprecation 警告，并不会
    改变任何行为，所以本文不再写这个字段。

!!! warning "请使用 `docker compose`，不要用 `docker-compose`"

    `docker-compose`（**带连字符**）是 **Python 版 v1** 的实现，**已于 2023 年停止维护**，不再
    获得安全更新。请使用 **Docker CLI v2 插件**：`docker compose`（**带空格**）。如果系统里两者
    都存在，请以 `docker compose` 为准，并尽早卸载 v1。

```yaml
name: todo-app

services:
  # 统一入口网关：反向代理到 frontend 与 backend
  nginx:
    image: nginx:1.25-alpine
    container_name: todo_nginx
    ports:
      - "8080:80"
    depends_on:
      frontend:
        condition: service_started
      backend:
        condition: service_healthy
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    command: >-
      sh -c '
      cat > /etc/nginx/nginx.conf <<"EOF"
      user  nginx;
      worker_processes  auto;
      events { worker_connections  1024; }
      http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;
        sendfile      on;
        keepalive_timeout  65;
        upstream frontend { server frontend:80; }
        upstream backend  { server backend:3001; }
        server {
          listen 80;
          location / { proxy_pass http://frontend; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
          location /api/ { rewrite ^/api/?(.*)$ /$1 break; proxy_pass http://backend; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; }
        }
      }
      EOF
      && nginx -g "daemon off;"'

  # 前端：无构建版 React（CDN 加载），由 nginx 直接静态托管
  frontend:
    image: nginx:1.25-alpine
    container_name: todo_frontend
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    command: >-
      sh -c '
      cat > /usr/share/nginx/html/index.html <<"EOF"
      <!doctype html>
      <html>
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Todo App</title>
          <style>
            body { font-family: ui-sans-serif, system-ui; max-width: 680px; margin: 24px auto; }
            li { display: flex; gap: 8px; align-items: center; padding: 6px 0; }
            button { cursor: pointer; }
          </style>
          <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
          <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        </head>
        <body>
          <h1>Todo App</h1>
          <div id="root"></div>
          <script>
            const e = React.createElement;
            const API_BASE = '/api';
            function App(){
              const [todos, setTodos] = React.useState([]);
              const [text, setText] = React.useState('');
              async function load(){
                const res = await fetch(`${API_BASE}/todos`);
                setTodos(await res.json());
              }
              async function add(){
                if(!text.trim()) return;
                await fetch(`${API_BASE}/todos`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ title: text })});
                setText('');
                load();
              }
              async function toggle(id, completed){
                await fetch(`${API_BASE}/todos/${id}`, { method:'PATCH', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ completed: !completed })});
                load();
              }
              async function remove(id){ await fetch(`${API_BASE}/todos/${id}`, { method:'DELETE' }); load(); }
              React.useEffect(()=>{ load(); },[]);
              return e('div', null,
                e('div', { style:{ display:'flex', gap:8 } },
                  e('input', { value:text, onChange:ev=>setText(ev.target.value), placeholder:'What to do?', style:{ flex:1, padding:8 } }),
                  e('button', { onClick:add }, 'Add')
                ),
                e('ul', null, todos.map(t => e('li', { key:t._id },
                  e('input', { type:'checkbox', checked:!!t.completed, onChange:()=>toggle(t._id, !!t.completed) }),
                  e('span', { style:{ textDecoration: t.completed ? 'line-through' : 'none' } }, t.title),
                  e('button', { style:{ marginLeft:'auto' }, onClick:()=>remove(t._id) }, 'Delete')
                )))
              );
            }
            ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
          </script>
        </body>
      </html>
      EOF
      && nginx -g "daemon off;"'

  # 后端：真实的工程结构，源码与 Dockerfile 都在 ./backend 下
  backend:
    build:
      context: ./backend
    image: todo-backend:local
    container_name: todo_backend
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/todos
      - PORT=3001
    depends_on:
      mongodb:
        condition: service_healthy
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    # 源码里提供了 /health 路由，用它做探活
    healthcheck:
      test: ["CMD", "node", "-e", "fetch('http://127.0.0.1:3001/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 30s

  # 数据库：官方 MongoDB
  mongodb:
    image: mongo:7
    container_name: todo_mongodb
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

volumes:
  mongodb_data:
```

!!! note "`nginx` 与 `frontend` 内的 heredoc 只是演示"

    上面把 `nginx.conf` 和 `index.html` 通过容器内命令内联生成，是为了让示例可以单文件运行、
    便于教学。真实工程里应当把它们拆成独立文件与各自的 Dockerfile，用 `build:` 构建，而不要在
    Compose 的 `command` 里拼源码——后端就是按正确做法展开的（见下一小节）。

### 后端工程文件

后端不应该把源码内联进 Compose 的 `command` 里。请在 `compose-demo/` 下创建 `backend/` 目录，
放入下面三个文件。

`backend/package.json`：

```json
{
  "name": "todo-backend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "cors": "2.x",
    "express": "4.x",
    "mongodb": "6.x"
  }
}
```

!!! note "`\"type\": \"module\"` 不能省"

    `server.js` 里用的是 ESM 的 `import` 语法。Node.js 只有在 package.json 声明
    `"type": "module"`（或把文件命名为 `.mjs`）时才会按 ESM 解析，否则启动会直接报
    `Cannot use import statement outside a module`。

`backend/server.js`：

```javascript
import express from "express";
import cors from "cors";
import { MongoClient, ObjectId } from "mongodb";

const app = express();
const port = process.env.PORT || 3001;
const mongoUri = process.env.MONGODB_URI || "mongodb://localhost:27017/todos";

app.use(cors());
app.use(express.json());

const client = new MongoClient(mongoUri);
let collection;

async function init(){
  await client.connect();
  const db = client.db();
  collection = db.collection("todos");
}

app.get("/health", (_req, res) => res.json({ ok: true }));

app.get("/todos", async (_req, res) => {
  const items = await collection.find({}).sort({ _id: -1 }).toArray();
  res.json(items);
});

app.post("/todos", async (req, res) => {
  const doc = { title: String(req.body?.title ?? ""), completed: false };
  const r = await collection.insertOne(doc);
  res.status(201).json({ _id: r.insertedId, ...doc });
});

app.patch("/todos/:id", async (req, res) => {
  const id = req.params.id; const body = req.body || {};
  await collection.updateOne({ _id: new ObjectId(id) }, { $set: body });
  const updated = await collection.findOne({ _id: new ObjectId(id) });
  if(!updated) return res.status(404).json({ message:"Not Found" });
  res.json(updated);
});

app.delete("/todos/:id", async (req, res) => {
  const id = req.params.id;
  await collection.deleteOne({ _id: new ObjectId(id) });
  res.status(204).end();
});

init().then(()=> app.listen(port, () => console.log(`API listening on ${port}`)))
  .catch(err => { console.error("Mongo connect error", err); process.exit(1); });
```

`backend/Dockerfile`：

```dockerfile
FROM node:22-alpine

WORKDIR /app

# 先复制依赖清单：依赖不变时这一层可以命中缓存
COPY package.json ./
RUN npm install --omit=dev

# 再复制源码：改代码不会让上面的依赖层失效
COPY server.js ./

EXPOSE 3001

CMD ["node", "server.js"]
```

### 配置与代码说明

- 统一入口 `nginx`：容器启动时写入 `nginx.conf` 并前台运行（演示写法，真实工程应拆成 Dockerfile）
- 前端 `frontend`：容器启动时生成 `index.html`，通过 CDN 加载 React，无需构建工具（同上）
- 后端 `backend`：由 `backend/Dockerfile` 构建成 `todo-backend:local` 镜像，源码与依赖清单都在
  `backend/` 目录下，通过 `npm install --omit=dev` 安装依赖后运行
- 数据库 `mongodb`：官方镜像，使用命名卷 `mongodb_data` 持久化数据
- 所有服务都带 `restart: unless-stopped` 与日志大小限制（`max-size: 10m` / `max-file: 3`），
  避免容器退出后不自愈、或日志无限增长把磁盘写满

### 服务解析

1. nginx 服务：使用官方 `nginx:1.25-alpine` 镜像，对外暴露 `8080:80`，将 `/` 转发到 `frontend`，`/api` 转发到 `backend`；通过 `depends_on` 等 `backend` 健康后再启动
1. frontend 服务：使用官方 `nginx:1.25-alpine`，启动时写入带 React CDN 的 `index.html`
1. backend 服务：使用 `backend/Dockerfile` 从 `node:22-alpine` 构建，安装依赖后运行 `server.js`，连接 `mongodb`；自带 `/health` 探活
1. mongodb 服务：使用官方 `mongo:7` 镜像，使用命名卷 `mongodb_data` 持久化；健康检查用 `mongosh --eval "db.adminCommand('ping')"` 判断是否就绪

### 网络与数据

- 网络：默认 bridge 网络，服务间通过服务名互访 (`nginx`、`frontend`、`backend`、`mongodb`)
- 数据：使用命名卷 `mongodb_data` 持久化 MongoDB 数据
- 依赖顺序：`backend` 用 `depends_on: mongodb: condition: service_healthy` 等待数据库就绪，
  而不是只等容器"被创建"；`nginx` 则等 `backend` 健康、`frontend` 启动

### 使用说明

1. 在后台启动服务（第一次运行需要构建后端镜像）：

```bash
docker compose up -d --build
```

2. 查看服务状态（`STATUS` 列出现 `healthy` 说明健康检查已通过）：

```bash
docker compose ps
```

3. 查看服务日志：

```bash
docker compose logs nginx
docker compose logs frontend
docker compose logs backend
docker compose logs mongodb
```

4. 停止所有服务：

```bash
docker compose down
```

5. 重新拉取镜像并重建容器：

```bash
docker compose pull && docker compose up -d --build --force-recreate
```

6. 重启单个服务：

```bash
docker compose restart frontend
```

### 访问应用

本地开发 (如 VS Code) 直接在浏览器打开 `http://localhost:8080` 即可访问 Todo 应用。

- 使用 VS Code Dev Containers/Remote - Containers 时，`8080` 端口通常会自动转发；也可在 Ports 面板手动添加端口转发
- 若端口被占用，可在 `compose.yaml` 中将 `8080:80` 改为其他可用端口 (如 `30080:80`)，然后重新启动：`docker compose up -d`
