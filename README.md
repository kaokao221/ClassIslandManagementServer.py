# 基于 Python 的适用于 [ClassIsland](https://github.com/classisland/classisland) 的集控服务器

集控服务器分为四个部分，分别是[`api`](./ManagementServer/api.py)[`command`](./ManagementServer/command.py)[`gRPC`](./ManagementServer/gRPC.py)[`WebUI`](./webui/README.md)，分别用于：

| 组件 | [`api`](./ManagementServer/api.py)   | [`command`](./ManagementServer/command.py) | [`gRPC`](./ManagementServer/gRPC.py) | [`WebUI`](./webui/README.md)     |
|----|--------------------------------------|--------------------------------------------|--------------------------------------|----------------------------------|
| 用途 | 向客户端分发配置文件                           | 通过API以集控服务器为中介获取客户端状态、向客户端发送指令             | 与客户端建立gRPC链接                         | 集控服务器网页前端（同时用作端口转发）              |
| 端口 | [50050](http://127.0.0.1:50050/docs) | [50052](http://127.0.0.1:50052/docs)       | 50051                                | [50053](http://localhost:50053/) |

## 如何使用？

以下是使用 ClassIsland 集控服务器的步骤：

1.  **环境准备**:
    *   **Python:** 确保你的系统已安装 Python 3.8+，推荐 Python 3.12+，推荐自行编译完整的 Python 3.12 & OpenSSL 3 环境。
    *   **Node.js and npm:** 如果你需要使用 WebUI，请确保已安装 Node.js (v22+) 和 npm。
    *   **Git (Optional):** 如果你想从 GitHub 克隆仓库，则需要安装 Git。
2.  **克隆代码:**
    ```bash
    git clone https://github.com/kaokao221/ClassIslandManagementServer.py.git
    cd ClassIslandManagementServer.py
    ```
    *   如果你不使用 Git，可以下载 ZIP 压缩包并解压。
3.  **创建 venv 并安装依赖:**
    ### 使用 uv （推荐）
    ```bash
    uv venv
    ./.venv/Scripts/activate # 进入venv
    uv pip install -r requirements.txt
    ```

    > ### 传统方法
    > ```bash
    > python -m venv venv
    > ./venv/bin/python -m pip install -r requirements.txt
    > # Windows 环境
    > ```
    > ```bash
    > python3 -m venv venv
    > ./venv/bin/python3 -m pip install -r requirements.txt
    > # Linux 环境
    > ```
    > 在 Linux 环境中，可能出现 venv / pip 不可用报错，请根据相关提示从命令行安装 venv 和 pip 后重新创建虚拟环境并安装依赖。
4. **构建 Protobuf 文件:**
    此步骤需要在venv中进行
    ```bash
    python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto
    # Windows 环境
    ```
    ```bash
    python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto
    # Linux 环境
    ```
    这将会构建 `.proto` 文件生成对应的 Python 代码，以用于 gRPC 通信。
5.  **构建 WebUI (可选):**
    *   如果你不需要 WebUI，可以跳过此步骤。
    *   安装NodeJS和pnpm （如果以安装可以跳过）

        Window:
        ```bash
        winget install nodejs
        # 重启终端
        corepack enable # 安装pnpm等工具
        ```
        Linux: 使用发行版的包管理工具安装nodejs，其他步骤与windows大体相同
    *   导航到 `webui` 目录:
        ```bash
        cd webui
        ```
    *   安装 WebUI 依赖:
        ```bash
        pnpm install
        ```
    *   构建 WebUI:
        ```bash
        pnpm build
        ```
    *   运行 WebUI:
        ```bash
        pnpm run preview
        ```
    *   构建完成后，将生成 `dist` 文件夹，其中包含构建后的 WebUI 文件。
    *   构建出的 WebUI 文件会被内置于集控服务器中，无需手动部署。
    * 结束构建后，返回根目录 `cd ..`
6.  **启动服务器:**
    *   **使用 `start.py` (第一次部署推荐):**
        ```bash
        ./venv/bin/python start.py
        # Windows 环境
        ```
        ```bash
        ./venv/bin/python3 start.py
        # Linux 环境
        ```
        这将启动一个引导，并启动所有服务器组件（gRPC、command、API）。
    *   **使用 `CIMS.py` (推荐):**
        ```bash
        ./venv/bin/python CIMS.py
        # Windows 环境
        ```
        ```bash
        ./venv/bin/python3 CIMS.py
        # Linux 环境
        ```
        或者，使用一些参数：
        ```bash
        ./venv/bin/python CIMS.py -g 50051 -a 50050 -m 50052
        ./venv/bin/python CIMS.py -l
        ./venv/bin/pythom CIMS.py -p
        # Windows 环境
        ```
        ```bash
        ./venv/bin/python3 CIMS.py -g 50051 -a 50050 -m 50052
        ./venv/bin/python3 CIMS.py -l
        ./venv/bin/pythom3 CIMS.py -p
        # Linux 环境
        ```
        这将提供更多的控制选项，例如:
        * `-c settings.json`: 从自定义的 `settings.json` 文件加载配置。
        * `-g 50051`: 将 gRPC 端口设置为 60000。
        * `-a 50050`: 将 API 端口设置为 60001。
        * `-m 50052`: 将 command 端口设置为 60002。
        * `-H 127.0.0.1`: 将 host 设置为 127.0.0.1。
        * `-l`: 列出当前的端口信息，不启动服务器。
        * `-p`: 生成 `ManagementPreset.json` 集控预设配置文件。
7.  **访问 WebUI:**
    *   如果已构建并启用了 WebUI，可以在浏览器中访问 `http://localhost:50053` (或你设置的端口)。
8. **访问 API:**
   * 你可以在浏览器中访问 `http://127.0.0.1:50050/docs` (或你设置的端口)查看 API 文档.

> ## 注意
> 目前所有的 README Guide 和 start.py 都是在 Windows 环境开发的，在 Linux 环境下已经有生产部署的先例，但在出现意料之外的问题时，还请在 commit 中提供更多诊断信息，谢谢！

## ~~功能清单~~

## Star 历史
[![Stargazers over time](https://starchart.cc/kaokao221/ClassIslandManagementServer.py.svg?variant=adaptive)](https://starchart.cc/kaokao221/ClassIslandManagementServer.py)