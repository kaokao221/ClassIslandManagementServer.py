# 基于 Python 的适用于 [ClassIsland](https://github.com/classisland/classisland) 的集控服务器

集控服务器分为四个部分，分别是[`api`](./ManagementServer/api.py)[`command`](./ManagementServer/command.py)[`gRPC`](./ManagementServer/gRPC.py)[`WebUI`](./webui/README.md)，分别用于：

| 组件 | [`api`](./ManagementServer/api.py)   | [`command`](./ManagementServer/command.py) | [`gRPC`](./ManagementServer/gRPC.py) | [`WebUI`](./webui/README.md)     |
|----|--------------------------------------|--------------------------------------------|--------------------------------------|----------------------------------|
| 用途 | 向客户端分发配置文件                           | 通过API以集控服务器为中介获取客户端状态、向客户端发送指令             | 与客户端建立gRPC链接                         | 集控服务器网页前端（同时用作端口转发）              |
| 端口 | [50050](http://127.0.0.1:50050/docs) | [50052](http://127.0.0.1:50052/docs)       | 50051                                | [50053](http://127.0.0.1:50053/) |

## 配置

运行 `python -m pip install -r requirements.txt` 以安装依赖

运行 `python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto` 以编译 `.proto` 文件

现在，你可以直接启动 [`main.py`](./main.py)，也可以到到 [`Notebook`](./ServerPresentation.ipynb) 阅读一些其它的相关信息。

> ***项目仍在建设过程中，如有疑问、需求请提 [commit](https://github.com/kaokao221/ClassIslandManagementServer.py/issues/new)，可以提交 [PR](https://github.com/kaokao221/ClassIslandManagementServer.py/compare)***
> 
> ***由于 [ClassIsland](https://github.com/classisland/classisland) 本身集控并未完工，服务器侧的刷新配置文件无法在发行版中生效，请注意***
>
> ***当前配置文件对接方式发生变更，相关的管理晚些时候上线***

## WebUI

请先 `cd webui`，在执行下面的命令之前

运行 `npm install` 安装依赖

运行 `npm run build` 构建生产环境的服务器

当前 WebUI 已经实现：
- [x] **概览页面**用于快速展示服务器已经注册的设备数量和在线的设备数量
- [x] **设备管理**用于向设备执行重启、推送消息和更新数据(更新数据客户端当前不支持，最早将在 1.7 版本上线)
- [ ] **配置文件管理**目前只实现基础的查看能力
- [ ] **设置**空的（

## 如何使用？

以下是使用 ClassIsland 集控服务器的步骤：

1.  **环境准备**:
    *   **Python:** 确保你的系统已安装 Python 3.7+。
    *   **Node.js and npm:** 如果你需要使用 WebUI，请确保已安装 Node.js (v16+) 和 npm。
    *   **Git (Optional):** 如果你想从 GitHub 克隆仓库，则需要安装 Git。
2.  **克隆代码:**
    ```bash
    git clone https://github.com/kaokao221/ClassIslandManagementServer.py.git
    cd ClassIslandManagementServer.py
    ```
    *   如果你不使用 Git，可以下载 ZIP 压缩包并解压。
3.  **安装依赖:**
    ```bash
    python -m pip install -r requirements.txt
    ```
    这将会安装 Python 相关的依赖。
4. **编译 Protobuf 文件:**
    ```bash
    python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto
    ```
    这将会编译 `.proto` 文件生成对应的 Python 代码，以用于 gRPC 通信。
5.  **构建 WebUI (可选):**
    *   如果你不需要 WebUI，可以跳过此步骤。
    *   导航到 `webui` 目录:
        ```bash
        cd webui
        ```
    *   安装 WebUI 依赖:
        ```bash
        npm install
        ```
    *   构建 WebUI:
        ```bash
        npm run build
        ```
    *   构建完成后，将生成 `dist` 文件夹，其中包含构建后的 WebUI 文件。
    *   构建出的 WebUI 文件会被内置于集控服务器中，无需手动部署。
    * 结束构建后，返回根目录 `cd ..`
6.  **启动服务器:**
    *   **使用 `main.py`:**
        ```bash
        python main.py
        ```
        这将以默认配置启动所有服务器组件（gRPC、command、API）。
    *   **使用 `CIMS.py` (推荐):**
        ```bash
        python CIMS.py
        ```
        或者，使用一些参数：
        ```bash
        python CIMS.py -c my_settings.json -g 60000 -a 60001 -m 60002 -H 127.0.0.1
        python CIMS.py -l
        ```
        这将提供更多的控制选项，例如:
        * `-c my_settings.json`: 从自定义的 `my_settings.json` 文件加载配置。
        * `-g 60000`: 将 gRPC 端口设置为 60000。
        * `-a 60001`: 将 API 端口设置为 60001。
        * `-m 60002`: 将 command 端口设置为 60002。
        * `-H 127.0.0.1`: 将 host 设置为 127.0.0.1。
        * `-l`: 列出当前的端口信息，不启动服务器。
7.  **访问 WebUI:**
    *   如果已构建并启用了 WebUI，可以在浏览器中访问 `http://localhost:50053` (或你设置的端口)。
8. **访问 API:**
   * 你可以在浏览器中访问 `http://127.0.0.1:50050/docs`(或你设置的端口)查看 API 文档.

## 功能清单

## Star 历史
[![Stargazers over time](https://starchart.cc/kaokao221/ClassIslandManagementServer.py.svg?variant=adaptive)](https://starchart.cc/kaokao221/ClassIslandManagementServer.py)