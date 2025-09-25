# Docker Compose 实践

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

在本章节中，我们通过一个最小可用的 Todo 应用来实战 Docker Compose 编排。示例完全基于官方镜像，并在容器启动时用命令动态生成所需配置与代码，不需要在本机创建除本文外的任何文件。

### 目标组件

- **Nginx**：统一入口与反向代理 (对外 8080)
- **前端**：CDN 版 React 静态页，由 Nginx 托管
- **后端**：Node.js Express API (容器内 3001)
- **数据库**：MongoDB (容器内 27017)

### 项目结构 (示意)

```text
5_compose/
└── docker-compose.yml    # Compose 配置（单文件示例）
```

### 3.3 架构图

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

### ocker Compose 配置

将下列 `docker-compose.yml` 内容复制到你的工程中使用 (该 compose 通过容器内命令动态生成 `nginx.conf`、前端 `index.html` 与后端 `server.js`)：

```yaml
version: "3.9"
name: todo-app

services:
  # 统一入口网关：反向代理到 frontend 与 backend
  nginx:
    image: nginx:1.25-alpine
    container_name: todo_nginx
    ports:
      - "8080:80"
    depends_on:
      - frontend
      - backend
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

  # 后端：Node.js（运行时安装依赖并生成 server.js）
  backend:
    image: node:18-alpine
    container_name: todo_backend
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/todos
      - PORT=3001
    depends_on:
      - mongodb
    command: >-
      sh -c '
      cat > server.js <<"EOF"
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
      EOF
      && npm init -y >/dev/null 2>&1 \
      && npm i express@4 cors@2 mongodb@6 --silent \
      && node server.js'

  # 数据库：官方 MongoDB
  mongodb:
    image: mongo:7
    container_name: todo_mongodb
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

### 配置与代码说明

- 统一入口 `nginx`：容器启动时写入 `nginx.conf` 并前台运行
- 前端 `frontend`：容器启动时生成 `index.html`，通过 CDN 加载 React，无需构建工具
- 后端 `backend`：容器启动时写入 `server.js`，随后安装依赖并运行
- 数据库 `mongodb`：官方镜像，使用命名卷 `mongodb_data` 持久化数据

### 服务解析

1. nginx 服务：使用官方 `nginx:alpine` 镜像，对外暴露 `8080:80`，将 `/` 转发到 `frontend`，`/api` 转发到 `backend`
1. frontend 服务：使用官方 `nginx:alpine`，启动时写入带 React CDN 的 `index.html`
1. backend 服务：使用官方 `node:18-alpine`，生成 `server.js`，安装依赖后运行，连接 `mongodb`
1. mongodb 服务：使用官方 `mongo:7` 镜像，使用命名卷 `mongodb_data` 持久化

### 网络与数据

- 网络：默认 bridge 网络，服务间通过服务名互访 (`nginx`、`frontend`、`backend`、`mongodb`)
- 数据：使用命名卷 `mongodb_data` 持久化 MongoDB 数据

### 使用说明

1. 在后台启动服务：

```bash
docker compose up -d
```

2. 查看服务状态：

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
docker compose pull && docker compose up -d --force-recreate
```

6. 重启单个服务：

```bash
docker compose restart frontend
```

### 访问应用

本地开发 (如 VS Code) 直接在浏览器打开 `http://localhost:8080` 即可访问 Todo 应用。

- 使用 VS Code Dev Containers/Remote - Containers 时，`8080` 端口通常会自动转发；也可在 Ports 面板手动添加端口转发
- 若端口被占用，可在 `docker-compose.yml` 中将 `8080:80` 改为其他可用端口 (如 `30080:80`)，然后重新启动：`docker compose up -d`
