# Docker 基础

## 安装 docker

默认于 Linux 系统环境下讲解 docker 的安装。docker 官方提供了一键式安装脚本，免去了手动安装的繁琐。

执行以下命令：

```shell
curl -fsSL https://get.docker.com | bash -s docker
```

可在此命令后附带--mirror 参数设置镜像源，以提高国内服务器下载 docker 的速度

如使用阿里云镜像：

```shell
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

接下来可使用如下命令来查看 docker 信息：

```shell
docker version  #查看版本信息
docker info     #查看运行时信息
```

## 运行你的第一个容器

```shell
docker run hello-world
```

跟所有的技术学习起点一样，上述命令使用 docker 运行一个最简单的 hello-world 容器，它的功能仅仅是在屏幕上打印一些文字。

`docker run` 首先会去本地寻找 hello-world 镜像，如果本地没有，则会从默认的 Docker 镜像仓库中拉去，也就是 [Docker Hub](https://hub.docker.com/)。

镜像的格式一般为

```text
<repository>/<image>:<tag>
```

如果 repository 为空，默认为 Docker Hub, tag 为空，则默认为 latest，
如下是一个 Nginx 镜像示例，其中 `repository` 为 library，
`image` 为 nginx，`tag` 为 1.25.3，这是从 Docker 官方仓库拉取特定版本的 Nginx 镜像。

```text
library/nginx:1.25.3
```

镜像分为 public 和 private 两种，对于 public 的镜像无需登录即可拉取，对于 private 的镜像则需要登录后才能拉取，登录命令如下

```shell
docker login <repository>
```

## 实践案例：运行 Alpine Linux 容器

Alpine 镜像在企业生产环境中被广泛应用，它是一个极简的 Linux 发行版，
只包含最基本的命令和工具，因此镜像非常小，只有 5MB 左右，并且内置包管理系统 `apk`, 使其成为许多其他镜像的常用起点。

拉取镜像

``` shell
docker pull alpine  #拉取镜像
docker image ls     #查看镜像
```

运行容器

``` shell
docker run alpine ls -a  #运行容器
docker ps -a             #查看容器
```

交互式运行容器

docker run 命令默认使用镜像中的 Cmd 作为容器的启动命令，Cmd 可通过如下命令来查看。

``` shell
docker inspect alpine --format='{{.Config.Cmd}}'
```

可以看到默认的 Cmd 为 `["/bin/sh"]`，因此直接使用 `docker run alpine` 会启动 /bin/sh 这个 shell,
我们 期望可以在这个 shell 中执行一些命令，但实际上它只是启动了 shell，退出了 shell，然后就停止了容器。

``` shell
docker run -it alpine  #等效于 docker run -it alpine /bin/sh, 使用 -it 参数启动容器进入交互式终端
```

后台运行容器

`run -it` 命令会启动一个交互式终端，退出终端后容器也会停止，如果希望容器在后台运行，可以使用 `-d` 参数，如下命令会启动一个后台运行的容器。

``` shell
docker run -it -d alpine #后台运行容器
```

加上 -d 参数后，容器不会执行完命令后立即退出，而是会进入后台运行，此时会返回一个唯一的 ID，使用 `docker ps` 命令可以查看容器运行状态。

docker attach 用于连接到一个正在运行的容器，主要作用是 访问容器的主进程（PID=1）的标准输入输出流

``` shell
docker attach <container_id>
```

由于 attach 是接管了 PID=1 的进程，因此如果这个进程是守护进程，
那么 attach 退出后，容器也会退出。所以一般不推荐使用 attach 命令。
而是使用 `docker exec` 命令来连接容器。

``` shell
docker exec -it <container_id> /bin/sh
```

此时进入到容器中使用 `ps -a` 命令可以看到容器中存在两个进程，其中 PID=1 的进程为 /bin/sh，
而另一个 /bin/sh 进程则是我们通过 exec 命令启动的，这个进程退出不会影响 PID=1 的进程，也就不会导致容器的退出。
