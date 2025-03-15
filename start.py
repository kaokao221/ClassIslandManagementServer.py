import os, sys, json, Datas

match sys.platform:
    case "win32":
        with open("settings.json", "w") as f:
            gRPC_port = input("gRPC 服务端口, 默认为 50051:")
            command_port = input("指令后端服务端口, 默认为 50052:")
            api_port = input("API 服务端口, 默认为 50050:")
            webui_port = input("WebUI 端口, <U默认为 50053:")
            json.dump({
                "ports": {
                    "gRPC": int(gRPC_port) if gRPC_port != "" else 50051,
                    "command": int(command_port) if command_port != "" else 50052,
                    "api": int(api_port) if api_port != "" else 50050,
                    "webui": int(webui_port) if webui_port != "" else 50053,
                },
                "organization_name": input("组织名称:"),
                "host": input("部署域名或IP, 本地测试请填 localhost:"),
            }, f)
            f.close()
        with open(input("配置文件已写入, 请提供预设的客户端三大金刚配置文件:"), "r") as d:
            default_confs = json.load(d)
            Datas.ClassPlan.write("default", {"ClassPlans": default_confs["ClassPlans"]})
            Datas.TimeLayout.write("default", {"TimeLayouts": default_confs["TimeLayouts"]})
            Datas.Subjects.write("default", {"Subjects": default_confs["Subjects"]})
        with open(input("三大金刚已写入, 请提供预设的客户端设置文件:"), "r") as s:
            default_sets = json.load(s)
            Datas.DefaultSettings.write("default", default_sets)
        os.system("python -m venv venv")
        os.system(".\\.venv\\Scripts\\pip install -r requirements.txt")
        os.system(".\\.venv\\bin\\python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto")
        os.system(".\\.venv\\bin\\python CIMS.py")
    case "linux":
        with open("settings.json", "w") as f:
            gRPC_port = input("gRPC 服务端口, 默认为 50051:")
            command_port = input("指令后端服务端口, 默认为 50052:")
            api_port = input("API 服务端口, 默认为 50050:")
            webui_port = input("WebUI 端口, <U默认为 50053:")
            json.dump({
                "ports": {
                    "gRPC": int(gRPC_port) if gRPC_port != "" else 50051,
                    "command": int(command_port) if command_port != "" else 50052,
                    "api": int(api_port) if api_port != "" else 50050,
                    "webui": int(webui_port) if webui_port != "" else 50053,
                },
                "organization_name": input("组织名称:"),
                "host": input("部署域名或IP, 本地测试请填 localhost:"),
            }, f)
            f.close()
        with open(input("配置文件已写入, 请提供预设的客户端三大金刚配置文件:"), "r") as d:
            default_confs = json.load(d)
            Datas.ClassPlan.write("default", {"ClassPlans": default_confs["ClassPlans"]})
            Datas.TimeLayout.write("default", {"TimeLayouts": default_confs["TimeLayouts"]})
            Datas.Subjects.write("default", {"Subjects": default_confs["Subjects"]})
        with open(input("三大金刚已写入, 请提供预设的客户端设置文件:"), "r") as s:
            default_sets = json.load(s)
            Datas.DefaultSettings.write("default", default_sets)
        os.system("python3 -m venv venv")
        os.system("./venv/Scripts/pip3 install -r requirements.txt")
        os.system("./venv/bin/python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. ./Protobuf/Client/ClientCommandDeliverScReq.proto ./Protobuf/Client/ClientRegisterCsReq.proto ./Protobuf/Command/HeartBeat.proto ./Protobuf/Command/SendNotification.proto ./Protobuf/Enum/CommandTypes.proto ./Protobuf/Enum/Retcode.proto ./Protobuf/Server/ClientCommandDeliverScRsp.proto ./Protobuf/Server/ClientRegisterScRsp.proto ./Protobuf/Service/ClientCommandDeliver.proto ./Protobuf/Service/ClientRegister.proto")
        os.system("./venv/bin/python3 CIMS.py")

