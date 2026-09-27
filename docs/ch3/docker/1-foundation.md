# Docker 基础

!!! note "主要作者"

    CAICAII

## 安装 Docker

不同操作系统和 Linux 发行版的安装方式不同，请优先按照 [Docker 官方安装文档](https://docs.docker.com/engine/install/)配置软件仓库并安装。通过软件仓库安装更便于后续升级和获取安全更新。

Docker 也提供面向测试与开发环境的便捷脚本。**不要把网络脚本直接通过管道交给 Shell**（例如
`curl ... | sh`）：管道执行意味着你没有任何机会检查脚本内容。正确的做法是"下载 → 阅读 → 校验
→ 执行"四步：

```bash
# 1. 下载：把脚本存成文件，而不是直接交给 shell
curl -fsSL https://get.docker.com -o get-docker.sh

# 2. 阅读：通读脚本，确认它改了哪些源、装了哪些包
less get-docker.sh

# 3. 校验：计算摘要，并与 Docker 官方页面公布的摘要比对
sha256sum get-docker.sh

# 4. 执行：先预览脚本将执行的操作，确认无误后再真正安装
sh get-docker.sh --dry-run
sudo sh get-docker.sh
```

确认脚本来源、内容和预览结果都适合当前测试环境后，再按官方文档执行安装。该脚本不推荐用于生产
环境，也不适合替代受控的版本和升级策略。

接下来可使用如下命令来查看 docker 信息：

```bash
docker version  # 查看版本信息
docker info     # 查看运行时信息
```

## 运行你的第一个容器

```bash
docker run hello-world
```

跟所有的技术学习起点一样，上述命令使用 docker 运行一个最简单的 hello-world 容器，它的功能仅仅是在屏幕上打印一些文字。

`docker run` 首先会去本地寻找 hello-world 镜像，如果本地没有，则会从默认的 Docker 镜像仓库中拉取，也就是 [Docker Hub](https://hub.docker.com/)。

镜像的格式一般为

```text
REPOSITORY/IMAGE:<tag>
```

如果 repository 为空，默认为 Docker Hub；tag 为空，则默认为 latest。
如下是一个 Nginx 镜像示例，其中 `repository` 为 library，
`image` 为 nginx，`tag` 为 1.25.3，这是从 Docker 官方仓库拉取特定版本的 Nginx 镜像。

```text
library/nginx:1.25.3
```

!!! warning "不要用 `latest`，先查镜像的支持周期再决定 tag"

    `latest` 并不是"最新稳定版"的保证，它只是上游维护者随手打的一个标签，会随上游发布而漂移：
    今天能构建、明天行为就可能不同，回滚时也无法确认当时用的是哪个版本。选 tag 的正确做法是：

    1. 打开 Docker Hub 上该镜像的页面，查看 **Tags** 列表，以及标签说明里指向的官方文档；
    2. 在上游项目的官方文档里找到它的 **release cycle / support（支持周期）** 页面，确认哪些
       系列仍在维护、哪些已经 EOL；
    3. 优先选择仍在维护的 LTS 或稳定系列，并**写死具体的小版本号或明确的系列标签**
       （例如 `nginx:1.25.3`、`mysql:8.4`），生产环境尤其不要依赖 `latest`。

镜像分为 public 和 private 两种，对于 public 的镜像无需登录即可拉取，对于 private 的镜像则需要登录后才能拉取，登录命令如下

```bash
docker login REPOSITORY
```

## 实践案例：运行 Alpine Linux 容器

Alpine 镜像在企业生产环境中被广泛应用，它是一个极简的 Linux 发行版，
只包含最基本的命令和工具，因此镜像非常小，只有 5MB 左右，并且内置包管理系统 `apk`，使其成为许多其他镜像的常用起点。

拉取镜像

```bash
docker pull alpine  # 拉取镜像
docker image ls     # 查看镜像
```

运行容器

```bash
docker run alpine ls -a  # 运行容器
docker ps -a             # 查看容器
```

交互式运行容器

docker run 命令默认使用镜像中的 Cmd 作为容器的启动命令，Cmd 可通过如下命令来查看。

```bash
docker inspect alpine --format='{{.Config.Cmd}}'
```

可以看到默认的 Cmd 为 `["/bin/sh"]`，因此直接使用 `docker run alpine` 会启动 /bin/sh 这个 shell，
我们期望可以在这个 shell 中执行一些命令，但实际上它只是启动了 shell，退出了 shell，然后就停止了容器。

```bash
docker run -it alpine  # 等效于 docker run -it alpine /bin/sh, 使用 -it 参数启动容器进入交互式终端
```

后台运行容器

`run -it` 命令会启动一个交互式终端，退出终端后容器也会停止，如果希望容器在后台运行，可以使用 `-d` 参数，如下命令会启动一个后台运行的容器。

```bash
docker run -it -d alpine  # 后台运行容器
```

加上 -d 参数后，容器不会执行完命令后立即退出，而是会进入后台运行，此时会返回一个唯一的 ID，使用 `docker ps` 命令可以查看容器运行状态。

docker attach 用于连接到一个正在运行的容器，主要作用是访问容器的主进程（PID=1）的标准输入输出流

```bash
docker attach CONTAINER_ID
```

由于 attach 是接管了 PID=1 的进程，因此如果这个进程是守护进程，
那么 attach 退出后，容器也会退出。所以一般不推荐使用 attach 命令。
而是使用 `docker exec` 命令来连接容器。

```bash
docker exec -it CONTAINER_ID /bin/sh
```

此时进入到容器中使用 `ps -a` 命令可以看到容器中存在两个进程，其中 PID=1 的进程为 /bin/sh，
而另一个 /bin/sh 进程则是我们通过 exec 命令启动的，这个进程退出不会影响 PID=1 的进程，也就不会导致容器的退出。

## 观察容器：从 `run` 到 `ps` 到 `logs`

前面几步都用 `-d` 把容器放到了后台，但我们怎么知道它到底跑起来没有？下面用一条完整链路来观察
一个容器从启动到出错的全过程。

```bash
# 启动一个后台运行的 nginx 容器，并给它起名字，方便后续引用
docker run -d --name demo -p 8080:80 nginx:1.25.3
```

用 `docker ps` 确认它是否在运行（`-a` 会连已停止的容器一起列出来）：

```bash
docker ps
```

```text
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
a1b2c3d4e5f6   nginx:1.25.3   "/docker-entrypoint.…"   5 seconds ago   Up 5 seconds   0.0.0.0:8080->80/tcp   demo
```

各列的含义：`CONTAINER ID` 是容器 ID 的短形式（前 12 位）；`IMAGE` 是启动时使用的镜像；
`STATUS` 里的 `Up 5 seconds` 说明容器正在运行（若是 `Exited (1) ...` 就说明它已经退出，括号里
是退出码）；`PORTS` 显示宿主机的 8080 映射到容器的 80；`NAMES` 就是我们用 `--name` 指定的名字，
后续命令既可以用容器 ID，也可以用这个名字。

如果容器起不来或行为异常，第一件事是看日志：

```bash
# 查看容器启动以来的全部日志
docker logs demo

# 实时跟踪（-f），并只显示最近 50 行（--tail）
docker logs -f --tail 50 demo
```

`docker logs` 读的是容器标准输出/标准错误的日志文件。默认的 `json-file` 日志驱动会把它写在
宿主机 `/var/lib/docker/containers/<容器 ID>/<容器 ID>-json.log`，而且**默认不做轮转**，长时间
运行的服务需要配置大小限制（见后面「容器监控与管理」一节）。

需要更细的状态时，用 `docker inspect` 读取容器的 JSON 元数据，配合 `-f` / `--format` 只取需要的
字段：

```bash
# 查看容器状态、退出码与是否被 OOM 杀死
docker inspect -f '{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}}' demo

# 查看容器实际拿到的 IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' demo
```

最后，停止并清理这个演示容器：

```bash
docker stop demo
docker rm demo
```

## 平台差异与 Docker Desktop 许可

Docker 在各平台上的安装方式并不相同：

- **Linux**：直接安装 Docker Engine（`docker-ce` + `containerd` + CLI）即可，容器与宿主机共用
  同一个内核，没有额外的虚拟化层，性能和网络行为最"原生"；
- **Windows**：需要 **WSL2 后端**（推荐，在 WSL2 的 Linux 发行版里跑 Engine）或旧的 Hyper-V
  后端；容器实际上跑在一个 Linux 虚拟机里；
- **macOS**：Docker Desktop 会在后台启动一台轻量 Linux 虚拟机来跑 Engine。因此 macOS 上
  `--network host` 之类依赖"宿主机网络栈"的特性行为与 Linux 不一致。

此外，Docker Desktop 的许可需要留意：**对员工数超过 250 人、或年收入超过 1000 万美元的商业
组织，Docker Desktop 需要付费订阅**；高校教学与个人使用是免费的。如果你所在的组织属于需要付费
的范围，又想避免授权问题，可以考虑这些替代方案：

- **Podman**：命令行与 Docker 高度兼容（`alias docker=podman` 基本可用），支持 rootless 容器，
  且无 Docker Desktop 的桌面端许可限制；
- **Colima**：macOS / Linux 上的开源容器运行时，提供与 `docker` CLI 兼容的接口，常被用作
  Docker Desktop 的免费替代；
- Linux 上也可以完全不装 Docker Desktop，直接用 Engine 或 Podman。

## 安全基线：非 root、只读根文件系统、capabilities

容器"能用"不等于"安全"。以下几件事是容器上生产前的底线：

**1. 不要以 root 运行进程。** 容器默认以 root 运行，一旦容器内的进程被攻破、或挂载了宿主机的
目录，影响会被放大。在 Dockerfile 里用 `USER` 切换到非 root 用户（见
[自定义镜像之 Dockerfile 详解](2-dockerfile.md)），或在运行时指定：

```bash
# 以 UID 1000 运行，覆盖镜像里的默认用户
docker run --user 1000:1000 nginx:1.25.3
```

**2. 尽量使用只读根文件系统。** 加上 `--read-only` 后，容器无法写自己的根文件系统，只保留显式
挂载或声明的可写位置：

```bash
# 根文件系统只读；需要写入的目录用 tmpfs 放在内存里。
# 官方 nginx 镜像启动时要写 /var/cache/nginx（临时目录）与 /var/run（PID 文件），
# 只挂 /tmp 会以 "Read-only file system" 退出。
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache/nginx \
  --tmpfs /var/run \
  nginx:1.25.3
```

!!! tip "只读根文件系统要先问清镜像需要写哪里"

    不同镜像需要写入的路径并不相同。做法是先跑一次，按报错补挂可写目录：例如
    `docker run --read-only <镜像> ...` 报 `Read-only file system: /var/cache/nginx`，
    就加 `--tmpfs /var/cache/nginx`。正规镜像通常会在文档里说明非 root / 只读运行的要求
    （例如提供 `nginx-unprivileged` 这类专门适配的变体）。

**3. 按最小权限裁剪 capabilities。** Linux capabilities 把 root 的特权拆成了若干细项，容器默认
仍带有不少能力。做法是先全部丢掉，再加回真正需要的：

```bash
# 丢光所有 capability，只加回绑定低端口所需的 NET_BIND_SERVICE
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx:1.25.3
```

**4. 不要用 `--privileged`。** `--privileged` 会关闭几乎所有隔离，等价于把宿主机 root 交给容器，
只应出现在明确知道后果的调试场景。

**5. 不要把 `/var/run/docker.sock` 挂进容器。** 能访问这个 socket 的进程就能在宿主机上创建任意
特权容器，等于拿到了宿主机 root：

```bash
# 反例：这会让容器获得等同宿主机 root 的能力，不要在生产使用
docker run -v /var/run/docker.sock:/var/run/docker.sock some-image
```
