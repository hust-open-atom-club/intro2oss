# Docker 网络管理详解

!!! note "主要作者"

    CAICAII

Docker 网络是容器通信的基础设施，它使容器能够安全地进行互联互通。在 Docker 中，每个容器都可以被分配到一个或多个网络中，容器可以通过网络进行通信，就像物理机或虚拟机在网络中通信一样。

## Docker 网络命令详解

在开始学习不同类型的网络之前，我们先来了解一下 Docker 的常用网络命令：

```bash
# 列出所有网络
docker network ls

# 检查网络详情
docker network inspect NETWORK_NAME

# 创建自定义网络
docker network create [options] NETWORK_NAME

# 将容器连接到网络
docker network connect NETWORK_NAME CONTAINER_NAME

# 断开容器与网络的连接
docker network disconnect NETWORK_NAME CONTAINER_NAME

# 删除网络
docker network rm NETWORK_NAME

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

```bash
mkdir -p nginx

cat > nginx/Dockerfile <<'EOF'
FROM nginx:1.25-alpine
RUN apk add --no-cache curl iputils
EOF

# 构建 nginx 镜像
docker build -t my-nginx nginx
```

```bash
# 查看默认 bridge 网络信息
docker network inspect bridge

# 启动两个容器
docker run -d --name container1 my-nginx
docker run -d --name container2 my-nginx

# 查看容器的网络配置
docker inspect container1 -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker inspect container2 -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 进入容器 1，尝试通过 IP 访问容器 2
docker exec -it container1 curl http://172.17.0.3

# 注意：在默认 bridge 网络中，无法通过容器名称访问
docker exec -it container1 curl http://container2  # 这将失败
```

!!! warning "不要照抄上面的 IP"

    `172.17.0.3` 只是某一次运行的示例值。默认 bridge 网络的地址是**按容器启动顺序动态分配**
    的，每次重建容器都可能变化。请先用 `docker inspect` 取到实际地址再访问：

    ```bash
    # 取出 container2 在 bridge 网络中的 IP（按上一步输出替换）
    CONTAINER2_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container2)

    # 再在 container1 里访问它
    docker exec -it container1 curl "http://${CONTAINER2_IP}"
    ```

Docker 默认的 bridge 网络存在通信限制：容器间只能通过易变的 IP 地址互相访问，无法使用固定的容器名称进行通信。
这种 IP 依赖会导致服务地址变更时需要人工调整配置，增加维护成本。通过创建自定义 bridge 网络，
容器可通过稳定的名称直接互访，这种自动化的服务发现机制正是 Docker Compose 实现容器编排的基础——编排工具会自动创建专用网络，
使多容器应用能够通过服务名称维持稳定的通信链路。

#### 实践案例二：自定义 Bridge 网络

现在让我们看看自定义 bridge 网络的优势：

```bash
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

!!! warning "`--network host` 在 Docker Desktop 上需要额外开启"

    `--network host` 在 **Linux 原生 Docker** 上开箱即用：容器直接复用宿主机的网络命名空间。
    Docker Desktop（macOS / Windows）早期版本**不支持**该模式——容器实际跑在一台轻量虚拟机里，
    `host` 指向的是那台虚拟机而不是你的宿主机。

    **Docker Desktop 4.34 及以上**可以在 `Settings → Resources → Network` 中启用
    **host networking**，启用后 Linux 容器即可用 `--network host` 直接访问宿主机服务（宿主机也能
    访问容器监听的端口）。若你的版本较旧或没有开启该开关，请改用 `-p` 显式发布端口：

    ```bash
    docker run -d --name nginx-port -p 80:80 my-nginx
    ```

    下面这段"端口冲突"的演示适用于 **Linux 原生环境，或已启用 host networking 的 Docker Desktop 4.34+**：两种情况都让容器直接复用宿主机网络，因此第二个容器会因端口被占用而启动失败。

实践案例：**使用 Host 网络运行 Nginx 服务器**

```bash
# 使用 host 网络运行 Nginx
docker run -d \
    --name nginx-host \
    --network host \
    my-nginx

# 直接通过主机的 80 端口访问
curl http://localhost:80

# 因为使用了 host 网络，容器直接使用主机的 80 端口，所以当我们再次启动一个 Nginx 容器时，会报端口冲突的错误
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

```bash
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

不过需要注意：**Docker Swarm 已经进入维护状态（maintenance mode）**，跨主机容器编排的主流方案
已经是 **Kubernetes**。现在新建项目基本不会再选 Swarm + Overlay，Overlay 网络主要出现在既有环境
和对 Docker 原生编排的学习中；如果要系统学习跨主机编排，建议直接学习 Kubernetes 的网络模型。

## 用 docker network inspect 读懂一个网络

排障时最常用的命令是 `docker network inspect`，它会把一个网络的完整配置以 JSON 输出。下面是一段
真实的输出结构（字段值随环境不同而变化）：

```json
[
    {
        "Name": "bridge",
        "Id": "8f4d2c1b9a0e7f3d5c6b4a2e1f0d9c8b7a6e5d4c3b2a1908f7e6d5c4b3a29180",
        "Created": "2024-05-01T10:00:00.000000000+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2": {
                "Name": "container1",
                "EndpointID": "1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3": {
                "Name": "container2",
                "EndpointID": "2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c4d5e6f1a2b3c",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```

关键字段逐条解读：

| 字段 | 含义 |
| --- | --- |
| `Name` / `Id` | 网络名与网络 ID，供 `docker network connect` / `rm` 引用 |
| `Scope` | `local` 表示只在本机生效；Overlay 网络这里是 `swarm` |
| `Driver` | 网络驱动：`bridge`、`host`、`overlay`、`macvlan`、`none` 等 |
| `EnableIPv6` | 是否启用了 IPv6 地址分配 |
| `IPAM.Config[].Subnet` | 这个网络的网段。默认 bridge 是 `172.17.0.0/16` |
| `IPAM.Config[].Gateway` | 网络网关，即宿主机上 `docker0` 网桥的地址 |
| `Internal` | 为 `true` 时该网络没有外部出口，只能容器间通信 |
| `Containers` | **当前接在这个网络上的容器**，键是容器 ID，值是它的 `Name` 与 `IPv4Address` |
| `Containers[].IPv4Address` | 容器在该网络内的地址（`/16` 是掩码长度），也就是用 `curl` 访问时该用的地址 |
| `Options` | 网桥级配置，例如 `com.docker.network.bridge.name` 就是 `docker0` 这个名字的来源 |

排障时可以直接用 `-f` 只取关心的部分，避免看一大段 JSON：

```bash
# 只看网段与网关
docker network inspect -f '{{range .IPAM.Config}}{{.Subnet}} gw={{.Gateway}}{{end}}' bridge

# 看谁接在这个网络上，以及各自的 IP
docker network inspect -f '{{range $id, $c := .Containers}}{{$c.Name}} -> {{$c.IPv4Address}}{{"\n"}}{{end}}' bridge
```
