# Docker 容器监控与管理

!!! note "主要作者"

    CAICAII

在本章节中，我们将学习如何有效地监控和管理 Docker 容器，包括使用命令行工具和图形化界面（Portainer）进行容器管理。

注意：该部分所需要的容器我们可以利用上一节 docker compose 出来的容器来演示。

## 容器管理基础

### 容器生命周期管理

以下是一些最常用的容器管理命令：

```bash
# 列出所有容器（包括停止的容器）
docker ps -a

# 仅列出运行中的容器
docker ps

# 启动容器
docker start CONTAINER_ID

# 停止容器
docker stop CONTAINER_ID

# 重启容器
docker restart CONTAINER_ID

# 删除容器（需要先停止）
docker rm CONTAINER_ID

# 强制删除运行中的容器
docker rm -f CONTAINER_ID
```

### 容器资源监控

Docker 提供了多种方式来监控容器的资源使用情况：

```bash
# 实时查看容器资源使用状态
docker stats

# 查看容器详细信息
docker inspect CONTAINER_ID

# 查看容器内进程
docker top CONTAINER_ID

# 查看容器端口映射
docker port CONTAINER_ID
```

## 容器日志与调试

### 日志查看

```bash
# 查看容器日志
docker logs CONTAINER_ID

# 实时查看最新日志
docker logs -f CONTAINER_ID

# 查看最近 100 行日志
docker logs --tail 100 CONTAINER_ID

# 显示时间戳
docker logs -t CONTAINER_ID
```

## 排障剧本：容器起不来 / 端口占用 / 磁盘写满

排障时不要一上来就翻文档。**先跑这三条命令**，绝大多数问题当场就能定位：

```bash
# 1. 容器到底在不在运行？退出码是多少？
docker ps -a

# 2. 应用自己说了什么？（最重要的一条）
docker logs --tail 50 CONTAINER_ID

# 3. 容器的详细状态：退出码、是否 OOM、端口映射、挂载了什么
docker inspect CONTAINER_ID
```

`docker ps -a` 的 `STATUS` 列会给出退出码，常见含义：

| 退出码 | 含义 | 一般原因 |
| --- | --- | --- |
| `0` | 正常结束 | 主进程执行完就退出了，容器里没有常驻服务（例如 `docker run alpine ls`） |
| `1` | 应用报错 | 代码抛异常、配置缺失、连不上数据库 |
| `137` | 被 `SIGKILL` 杀死 | 最常见的是 **OOM**（内存超限），也可能是 `docker kill` |
| `143` | 被 `SIGTERM` 终止 | `docker stop` 发出的正常信号；若反复出现，说明进程没处理好优雅退出 |

### 分支一：容器起不来 / 起来就退出

```bash
# 看退出码和状态原因
docker inspect -f 'status={{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} error={{.State.Error}}' CONTAINER_ID

# 看最后 50 行日志
docker logs --tail 50 CONTAINER_ID

# 直接前台跑一次，把报错暴露在终端里
docker run --rm -it IMAGE sh
```

注意：如果日志一行都没有，说明进程在启动阶段就崩了，或者镜像的 `CMD` / `ENTRYPOINT` 写错了。
用 `-d` 启动时看不到进程启动前的报错，直接在终端里不带 `-d` 跑一次往往最快看到真相。

### 分支二：端口占用（`bind: address already in use`）

```bash
# 看这个容器实际发布了哪些端口
docker port CONTAINER_ID

# 看宿主机的 8080 被谁占了（二选一，取决于系统里装了哪个）
ss -lntp | grep :8080
lsof -i :8080
```

处理方式有两种，按推荐顺序排列：

1. **换一个宿主机端口**：把 `-p 8080:80` 改成 `-p 30080:80`（容器内端口不用动）；
2. **停掉占用端口的那个进程/容器**：用 `docker ps` 找到占用者后 `docker stop`。

!!! warning "`--network host` 不是端口冲突的解决办法"

    不要想着"用 `--network host` 绕过端口占用"：这个模式让容器进程**直接绑定宿主机端口**，
    端口被占用时同样会以 `address already in use` 启动失败（[Docker 网络管理详解](4-network.md)
    里的两个 `host` 网络 Nginx 实验，正是用第二个容器启动失败来说明这一点）。

### 分支三：磁盘写满（`no space left on device`）

```bash
# 先看清楚是谁占的空间：镜像、容器还是卷
docker system df

# 想看更细的明细（每个镜像/容器/卷各自多大）
docker system df -v
```

确认之后按下面的顺序逐步清理，每一步都先看清将删除什么：

```bash
# 1. 删除所有已停止的容器
docker container prune

# 2. 删除悬空镜像（没有 tag 的中间层）与构建缓存
docker image prune
docker builder prune

# 3. 需要时再删除没有被任何容器使用的镜像
docker image prune -a
```

!!! danger "慎用 `docker system prune -a --volumes`"

    `docker system prune -a --volumes` 会删除所有未使用的镜像、容器、网络**以及数据卷**。
    数据卷里通常装着数据库文件，删掉就再也找不回来了。清理磁盘前务必先用 `docker system df -v`
    确认，并单独备份需要保留的卷。

## 资源限制与 OOM

默认情况下容器可以吃掉宿主机全部内存和 CPU，一个失控的容器就能把整台机器拖垮。生产环境应当显式
限制资源：

| 参数 | 含义 |
| --- | --- |
| `--memory` | 容器可用的内存上限（如 `512m`、`2g`）。超限时内核的 OOM killer 会杀掉容器内进程 |
| `--memory-swap` | 内存 + swap 的总上限。设为**与 `--memory` 相等**表示禁用 swap；不设时默认是 `--memory` 的两倍 |
| `--cpus` | CPU 核数上限，可以是小数（`1.5` 表示最多用 1.5 个核） |
| `--pids-limit` | 容器内进程/线程数上限，防止 fork bomb 把宿主机拖死 |

```bash
# 限制为最多 512MB 内存（禁用 swap）、1.5 个 CPU
docker run -d --name limited \
    --memory 512m --memory-swap 512m \
    --cpus 1.5 \
    --pids-limit 200 \
    nginx:1.25.3
```

用 `docker stats` 观察实时用量，各列含义如下：

```text
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O   PIDS
a1b2c3d4e5f6   limited   0.15%     24.5MiB / 512MiB      4.79%     1.2kB / 0B    0B / 0B     9
```

- `MEM USAGE / LIMIT`：当前用量 / 你设置的上限。**接近 LIMIT 就是要出事的前兆**；
- `MEM %`：用量占上限的百分比；持续攀升说明有内存泄漏或缓存没有回收；
- `CPU %`：相对**单个核**的百分比，超过 100% 说明用到了多个核（受 `--cpus` 约束）；
- `PIDS`：容器内当前进程/线程数，配合 `--pids-limit` 一起看。

容器被 OOM 杀掉时有三个特征：

```bash
# 1. 退出码是 137
docker ps -a

# 2. OOMKilled 标记为 true
docker inspect -f '{{.State.OOMKilled}}' CONTAINER_ID

# 3. 宿主机内核日志里能看到 oom-killer 记录
dmesg | tail -20
```

!!! note "调大内存不是唯一答案"

    遇到 OOM 时，先确认是**限制太小**还是**程序真的泄漏**：用 `docker stats` 观察一段时间，
    如果内存单调上涨、从不回落，通常是程序问题，直接调大 `--memory` 只会把问题推迟。
    另外 JVM / Node.js 之类的运行时需要额外留出堆外内存，限制值应比应用配置的堆上限更大一些。

## 日志驱动与磁盘占用

Docker 默认使用 **`json-file` 日志驱动**，把容器的标准输出/标准错误写在
`/var/lib/docker/containers/<容器 ID>/<容器 ID>-json.log`。问题在于：**默认不轮转**，一个不停
打日志的服务可以轻松把磁盘写满。

```bash
# 启动时限制单个日志文件最大 10MB，最多保留 3 个（总计约 30MB）
docker run -d \
    --log-driver json-file \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    nginx:1.25.3

# 查看容器当前使用的日志驱动与选项
docker inspect -f '{{.HostConfig.LogConfig}}' CONTAINER_ID

# 查看 Docker 占用的磁盘总量
docker system df
```

几个要点：

- `docker logs` 读的就是 `json-file` 里的内容，所以日志文件被清空后 `docker logs` 也会变空；
- 想让**所有**容器默认带轮转，可以在 daemon 的 `daemon.json` 里统一配置，而不是每个
  `docker run` 手写一遍：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

- 改动 daemon 配置后需要重启 Docker 服务，且**只对新建的容器生效**；
- 如果日志本身不重要（例如只是访问日志），也可以换成 `local` 或 `none` 驱动，或把日志直接送到
  集中式日志系统，避免占用宿主机磁盘。

在 Compose 里，这些选项写在每个服务的 `logging` 段下（示例见
[Docker Compose 实践](5-compose.md)）。

## 实践练习：使用 Portainer 对 Docker 进行可视化管理

Portainer 是一个轻量级的 Docker 管理工具，提供了直观的 Web 界面来管理 Docker 环境。

### 安装 Portainer

```bash
# 创建 Portainer 数据卷
docker volume create portainer_data

# 运行 Portainer 容器（本地访问 http://localhost:9000）
docker run -d -p 9000:9000 \
    --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

!!! note "关于 `portainer/portainer-ce:lts` 这个标签"

    `lts` 是 Portainer 官方提供的长期支持标签，教材编写时对应 **2.x LTS 系列**。使用 `lts`
    可以自动跟随该 LTS 系列的小版本更新，而不必每次手工改版本号。如果你需要完全可复现的环境，
    也可以把它换成某个具体的小版本号。

!!! warning "挂载 docker.sock 等于交出宿主机控制权"

    上面把 `/var/run/docker.sock` 挂进容器的做法，是 Portainer 正常工作的前提，但也意味着这个
    容器**可以控制宿主机上的 Docker**（等价于宿主机 root 权限）。因此 Portainer 只应部署在受控
    环境（本机开发、可信内网），并务必设置强管理员口令、不要把它暴露到公网。

在本地/VS Code 环境下，打开浏览器访问 `http://localhost:9000` 即可进入 Portainer 初始化页面。首次登录会创建管理员账户。

- VS Code Dev Containers/Remote - Containers 下，端口通常会自动转发；也可在 Ports 面板手动转发 9000 端口
- 若端口被占用，可改为 `-p 39000:9000`，然后通过 `http://localhost:39000` 访问

### Portainer 主要功能

1. **仪表盘概览**
   - 查看环境整体状态
   - 监控资源使用情况
   - 查看事件日志

2. **容器管理**
   - 创建、启动、停止、删除容器
   - 查看容器日志和统计信息
   - 进入容器终端（Console）
   - 修改容器配置

3. **镜像管理**
   - 拉取和删除镜像
   - 构建新镜像
   - 推送镜像到仓库

4. **网络管理**
   - 创建和管理 Docker 网络
   - 配置容器网络连接

5. **数据卷管理**
   - 创建和删除数据卷
   - 管理数据卷权限
