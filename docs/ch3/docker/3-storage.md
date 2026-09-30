# Docker 存储管理详解

!!! note "主要作者"

    CAICAII

Docker 容器在运行时会产生大量数据，这些数据如何持久化和管理是一个重要的话题。
本节我们将通过一个 Nginx Web 服务器的案例，来深入探讨 Docker 的三种数据管理方式。

## Docker 存储基础

Docker 提供了三种主要的数据管理方式：

1. **默认存储**：容器内的数据随容器删除而丢失
2. **Volumes（卷）**：由 Docker 管理的持久化存储空间，完全独立于容器的生命周期
3. **Bind Mounts（绑定挂载）**：将主机上的目录或文件直接挂载到容器中

让我们通过一个 Nginx Web 服务器的例子来理解这三种方式的区别。我们将在每种方式下执行相同的操作：创建一个 HTML 文件，然后测试数据的持久性。


### 场景一：默认存储（非持久化）

在这个场景中，我们直接在容器内创建文件，看看数据会发生什么：

```bash
# 运行一个 nginx 容器
docker run -d --name web-default -p 8000:80 nginx

# 在容器中创建一个测试页面
docker exec -it web-default sh -c 'echo "<h1>Hello from Default Storage</h1>" > /usr/share/nginx/html/index.html'

# 访问页面验证内容
curl http://localhost:8000

# 删除容器
docker rm -f web-default

# 用同样的配置重新运行容器
docker run -d --name web-default -p 8000:80 nginx

# 再次访问页面，会看到默认的 Nginx 欢迎页面，之前的内容已经丢失
curl http://localhost:8000
```

### 场景二：使用 Volume

在这个场景中，我们使用 Docker 管理的卷来存储数据：

```bash
# 创建一个 Docker volume
docker volume create nginx_data

# 运行 Nginx 容器并挂载卷
docker run -d --name web-volume -p 8081:80 -v nginx_data:/usr/share/nginx/html nginx

# 在容器中创建一个测试页面
docker exec -it web-volume sh -c 'echo "<h1>Hello from Volume Storage</h1>" > /usr/share/nginx/html/index.html'

# 访问页面验证内容
curl http://localhost:8081

# 删除容器
docker rm -f web-volume

# 用同样的配置重新运行容器
docker run -d --name web-volume-2 -p 8081:80 \
   -v nginx_data:/usr/share/nginx/html nginx

# 再次访问页面，内容仍然存在
curl http://localhost:8081

# 查看卷的详细信息
docker volume inspect nginx_data
```

### 场景三：使用 Bind Mount

在这个场景中，我们将主机上的目录直接挂载到容器中：

```bash
# 创建本地目录
mkdir nginx-content
echo "<h1>Hello from Bind Mount Storage</h1>" > nginx-content/index.html

# 运行 Nginx 容器并挂载本地目录
docker run -d --name web-bind \
   -p 8082:80 \
   -v $(pwd)/nginx-content:/usr/share/nginx/html nginx

# 访问页面验证内容
curl http://localhost:8082

# 在主机上修改文件
echo "<h1>Updated content from host</h1>" > nginx-content/index.html

# 无需重启容器，直接访问更新后的内容
curl http://localhost:8082

# 删除容器
docker rm -f web-bind

# 用同样的配置重新运行容器
docker run -d --name web-bind-2 -p 8082:80 \
   -v $(pwd)/nginx-content:/usr/share/nginx/html nginx

# 再次访问页面，内容仍然存在
curl http://localhost:8082
```

### 三种方式的对比

1. **默认存储**
    - 数据随容器删除而丢失
    - 适合存储临时数据
    - 容器间数据隔离
    - 无需额外配置

2. **Volume**
    - 数据持久化，独立于容器生命周期
    - Docker 统一管理，方便备份和迁移
    - 可以在多个容器间共享
    - 数据存储在 Docker 管理区域，安全性好

3. **Bind Mount**
    - 数据持久化，存储在主机指定位置
    - 可以直接在主机上修改文件
    - 开发环境中方便调试和修改
    - 依赖主机文件系统结构

### 清理操作

完成实验后，可以进行清理：

!!! danger "下面的命令会永久删除数据"

    这条清理流程会删除本次实验创建的容器、命名卷 `nginx_data` 以及本地目录
    `nginx-content`，**内容不可恢复**。执行前请确认：

    - 你确实在实验目录下（`pwd`），`rm -rf nginx-content` 只作用于本节创建的那个目录；
    - `nginx_data` 与 `nginx-content` 中没有你后来放进去、还想保留的内容；
    - 如果卷名与其它项目重名，请先 `docker volume ls` 确认，不要直接照抄。

```bash
# 清理本次实验的容器（只会删掉这些名字的容器）
docker rm -f web-default web-volume web-volume-2 web-bind web-bind-2

# 清理本次实验创建的命名卷（其中的数据将永久丢失）
docker volume rm nginx_data

# 清理本次实验创建的本地目录（确认当前目录是实验目录后再执行）
rm -rf nginx-content
```

## 实践案例：使用 Volume 部署 MySQL 数据库

我们将通过一个 MySQL 数据库的例子来演示如何使用 Volume 持久化数据。

!!! warning "数据库镜像必须钉死小版本，不要用 `latest`"

    MySQL / MongoDB 这类数据库在**跨大版本升级时会改动数据目录的格式**。如果你用的是
    `mysql:latest` 或 `mysql:8` 这种浮动标签，某天重新拉取镜像时可能把旧版本写下的数据目录
    交给一个不兼容的新版本去打开，结果就是容器起不来、甚至数据损坏。

    正确做法是**钉死到明确的小版本**（本文统一使用 `mysql:8.4`），并且升级前先备份数据卷，
    按官方文档的升级路径操作（可能需要先升到中间版本、再执行 `mysql_upgrade` 之类的步骤），
    不要依赖 `latest` 自动升级。

### 创建并管理 Volume

```bash
# 创建一个命名卷
docker volume create mysql_data

# 查看卷信息
docker volume inspect mysql_data

# 列出所有卷
docker volume ls
```

### 使用 Volume 运行 MySQL

```bash
# 先定义一个仅用于本地实验的 root 口令（生产环境不要这样写，见下面的提示框）
export MYSQL_ROOT_PASSWORD='mysecret'

# 运行 MySQL 容器并挂载卷
docker run -d \
  --name mysql_db \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
  -v mysql_data:/var/lib/mysql \
  mysql:8.4

# 等数据库真正就绪再连接：docker run -d 只是把容器放到后台，不会等 MySQL 初始化完成，
# 首次启动（要初始化数据目录）通常需要十几秒，立刻连接会得到 "Can't connect to MySQL server"。
until docker exec mysql_db mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD" --silent >/dev/null 2>&1; do
  echo "等待 MySQL 就绪…"; sleep 3
done

# 进入容器创建测试数据（口令必须与上面的变量一致）
docker exec -it mysql_db mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -h127.0.0.1
```

进入 MySQL 交互界面后（`mysql>` 是 MySQL 自己的提示符，不是 shell 提示符）：

```text
mysql> CREATE DATABASE test_db;
mysql> USE test_db;
mysql> CREATE TABLE users (id INT, name VARCHAR(50));
mysql> INSERT INTO users VALUES (1, 'John Doe');
mysql> exit
```

!!! warning "口令只用于本地实验"

    上面用 `export` 定义 `mysecret` 只是为了让命令能直接跑通。需要注意两点：

    - 通过 `-e` 在命令行上传入口令，会同时留在 shell 历史记录、`docker inspect` 的输出以及进程
      参数里，任何能执行 `docker` 命令的用户都能看到；
    - 首次初始化后，`MYSQL_ROOT_PASSWORD` 会被忽略——后面重用同一个数据卷时必须使用**同一个**口令。

    生产环境请改用 `--env-file`（并限制文件权限）或 secret 机制，不要使用示例口令。

### 验证数据持久化

```bash
# 删除原容器
docker rm -f mysql_db

# 使用同一个卷启动新容器（口令与前面保持一致；数据卷已初始化，此变量不会再被使用）
docker run -d \
  --name mysql_db2 \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
  -v mysql_data:/var/lib/mysql \
  mysql:8.4

# 同样要等服务就绪（这一步同样存在竞态，不能紧接着就连接）
until docker exec mysql_db2 mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD" --silent >/dev/null 2>&1; do
  echo "等待 MySQL 就绪…"; sleep 3
done

# 验证数据是否存在
docker exec -it mysql_db2 \
   mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "USE test_db; SELECT * FROM users;"
```

## -v 与 --mount 的区别

Docker 提供了两种挂载语法：`-v`（`--volume`）和 `--mount`。两者都能挂载卷与宿主机目录，但
**推荐使用 `--mount`**，因为它的语义更明确，出错时也更容易发现：

- `-v` 的参数是"三段式"的 `源:目标[:选项]`，写错很难察觉；
- **`-v` 在宿主机路径不存在时会静默创建目录**。例如你想挂载一个配置文件，却把路径拼错了：

```bash
# 危险：若 ./nginx.conf 拼写错误（比如写成 ./ngnix.conf），Docker 会静默创建一个同名
# "目录"挂进去，容器能启动，但读到的并不是你的配置文件
docker run -d -p 80:80 \
    -v $(pwd)/ngnix.conf:/etc/nginx/nginx.conf:ro \
    nginx:1.25-alpine
```

而 `--mount` 用命名的键值对描述挂载，源路径不存在时会直接报错，不会替你"猜"：

```bash
# 卷：由 Docker 管理，卷不存在会自动创建
docker run -d \
    --mount type=volume,src=nginx_data,dst=/usr/share/nginx/html \
    nginx:1.25-alpine

# 绑定挂载：源路径必须存在，写错立刻报错
docker run -d \
    --mount type=bind,src=$(pwd)/nginx-content,dst=/usr/share/nginx/html,readonly \
    nginx:1.25-alpine

# 内存文件系统：数据只放在内存里
docker run -d \
    --mount type=tmpfs,dst=/tmp \
    nginx:1.25-alpine
```

补充说明：

- `--mount` 的 `readonly` 选项等价于 `-v` 结尾的 `:ro`；
- `-v` 在 `docker run` 和 Compose 文件里仍然非常常见（Compose 中通常写作 `volumes:` 短语法），
  读别人的配置时要能看懂两种写法；
- 卷名如果不存在，两种写法都会自动创建**卷**；只有 `bind` 类型的宿主机目录/文件不存在时行为
  不同：`-v` 静默建目录，`--mount` 报错。

## tmpfs：把敏感数据留在内存

有些数据既需要"像文件一样"被读写，又**完全不应该落盘**，例如临时密钥、会话文件、解密后的凭据。
这时可以用 `tmpfs` 挂载：它把数据放在内存里，容器停止后内容立即消失，也不会出现在镜像层或
数据卷中。

```bash
# 把一个 16MB 的内存文件系统挂到容器的 /run/secrets
docker run --rm -it \
    --mount type=tmpfs,destination=/run/secrets,tmpfs-size=16m \
    alpine:3.21 sh
```

也可以用更简短的 `--tmpfs` 写法：

```bash
# 根文件系统只读时，用 tmpfs 提供容器真正需要的可写目录
# （官方 nginx 镜像要写 /var/cache/nginx 与 /var/run）
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache/nginx \
  --tmpfs /var/run \
  nginx:1.25-alpine
```

要点：

- 数据不落盘，容器停止即消失，适合**临时**敏感数据；
- **不适合需要持久化的数据**：重启容器内容就没了；
- 会占用容器的内存配额，所以 `tmpfs-size` 要设得合理——在限制内存的容器里开一个巨大的 tmpfs
  可能直接把容器 OOM；
- 与"把密钥写进环境变量"相比，tmpfs 更适合放**文件形式**的凭据（如证书、私钥）。
