# Docker 网络管理详解

Docker 网络是容器通信的基础设施，它使容器能够安全地进行互联互通。在 Docker 中，每个容器都可以被分配到一个或多个网络中，容器可以通过网络进行通信，就像物理机或虚拟机在网络中通信一样。

## Docker 网络命令详解

在开始学习不同类型的网络之前，我们先来了解一下 Docker 的常用网络命令：

```shell
# 列出所有网络
docker network ls

# 检查网络详情
docker network inspect <network-name>

# 创建自定义网络
docker network create [options] <network-name>

# 将容器连接到网络
docker network connect <network-name> <container-name>

# 断开容器与网络的连接
docker network disconnect <network-name> <container-name>

# 删除网络
docker network rm <network-name>

# 删除所有未使用的网络
docker network prune
```

## 网络类型及实践案例

### 1. Bridge 网络（桥接网络）

Bridge 网络是 Docker 的默认网络驱动程序。当你创建一个容器而不指定网络时，它会自动添加到默认的 `bridge` 网络中。Bridge 网络在单机环境下使用非常广泛，它通过软件网桥实现容器间的通信。

#### Bridge 网络的工作原理

Bridge 网络就像是 Docker 中的一个虚拟交换机，它在宿主机上创建一个名为 docker0 的网桥，
所有连接到这个网桥的容器都可以通过它进行通信。当你安装 Docker 时，会自动创建一个默认的 bridge 网络，
它一般使用 172.17.0.0/16 这个网段，所有未指定网络的容器都会自动连接到这个默认网络中。
不过，默认的 bridge 网络功能比较简单，容器之间只能通过 IP 地址互相访问，不支持通过容器名称来通信。

为了解决这个限制，Docker 提供了用户自定义 bridge 网络的功能。
当你创建自己的 bridge 网络时，连接到这个网络的容器就能获得更多便利的特性：容器之间可以通过名称相互访问，
网络隔离性更好，还可以随时将容器从网络中添加或移除。这就像是给容器们创建了一个独立的局域网，
既安全又方便管理。比如说，你可以把一个应用的前端、后端和数据库容器都放在同一个自定义 bridge 网络中，
它们就能通过容器名称轻松地相互通信，同时又与其他应用的容器网络保持隔离。

#### 实践案例一：默认 Bridge 网络

让我们先来看看默认 bridge 网络的行为：

我们现构建一个装有 ping, curl 等指令的 nginx 镜像，方便我们在容器内容观察网络行为。

```shell
mkdir -p nginx

cat > nginx/Dockerfile <<'EOF'
FROM nginx:alpine
RUN apk add --no-cache curl iputils
EOF

# 构建 nginx 镜像
docker build -t my-nginx nginx
```

```shell
# 查看默认 bridge 网络信息
docker network inspect bridge

# 启动两个容器
docker run -d --name container1 my-nginx
docker run -d --name container2 my-nginx

# 查看容器的网络配置
docker inspect container1 -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker inspect container2 -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 进入容器1，尝试通过 IP 访问容器2
docker exec -it container1  curl http://172.17.0.3

# 注意：在默认 bridge 网络中，无法通过容器名称访问
docker exec -it container1  curl http://container2  # 这将失败
```

Docker 默认的 bridge 网络存在通信限制：容器间只能通过易变的 IP 地址互相访问，无法使用固定的容器名称进行通信。
这种 IP 依赖会导致服务地址变更时需要人工调整配置，增加维护成本。通过创建自定义 bridge 网络，
容器可通过稳定的名称直接互访，这种自动化的服务发现机制正是 Docker Compose 实现容器编排的基础——编排工具会自动创建专用网络，
使多容器应用能够通过服务名称维持稳定的通信链路。

#### 实践案例二：自定义 Bridge 网络

现在让我们看看自定义 bridge 网络的优势：

```shell
# 创建自定义 bridge 网络
docker network create \
    --driver bridge \
    --subnet=172.20.0.0/16 \
    --gateway=172.20.0.1 \
    my-bridge-network

# 启动两个容器，连接到自定义网络
docker run -d \
    --name custom-container1 \
    --network my-bridge-network \
    my-nginx

docker run -d \
    --name custom-container2 \
    --network my-bridge-network \
    my-nginx

# 现在可以通过容器名称访问
docker exec -it custom-container1 curl http://custom-container2
```

### 2. Host 网络

Host 网络移除了容器和 Docker 主机之间的网络隔离，直接使用主机的网络。

**特点：**

- 最佳网络性能
- 直接使用主机的网络栈
- 没有网络隔离
- 端口直接绑定到主机上

实践案例：**使用 Host 网络运行 Nginx 服务器**

```shell
# 使用 host 网络运行 Nginx
docker run -d \
    --name nginx-host \
    --network host \
    my-nginx

# 直接通过主机的 80 端口访问
curl http://localhost:80

# 因为使用了 host 网络，容器直接使用主机的 80 端口, 所以当我们再次启动一个 Nginx 容器时，会报端口冲突的错误
docker run -d \
    --name nginx-host-2 \
    --network host \
    my-nginx
    
docker logs nginx-host-2
```

### 3. None 网络

None 网络完全禁用了容器的网络功能，容器在这个网络中没有任何外部网络接口。

**特点：**

- 完全隔离的网络环境
- 容器没有网络接口
- 适用于不需要网络的批处理任务

实践案例：**使用 None 网络运行独立计算任务**

```shell
# 运行一个计算密集型任务，不需要网络
docker run --network none alpine sh -c 'for i in $(seq 1 10); do echo $((i*i)); done'
```

### 4. Overlay 网络

Overlay 网络是 Docker 用于实现跨主机容器通信的网络驱动，主要用于 Docker Swarm 集群环境。
它通过在不同主机的物理网络之上创建虚拟网络，使用 VXLAN 技术在主机间建立隧道，从而实现容器间的透明通信。
在 Overlay 网络中，每个容器都会获得一个虚拟 IP，容器之间可以直接通过这个 IP 进行通信，
而不需要关心容器具体运行在哪个主机上。这种网络类型特别适合于微服务架构、分布式应用以及需要跨主机通信的容器化应用，
例如分布式数据库集群、消息队列集群等。Overlay 网络支持网络加密，能确保跨主机通信的安全性，
同时还提供了负载均衡和服务发现等特性，是构建大规模容器集群的重要基础设施。