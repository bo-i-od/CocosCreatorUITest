'''
Author: zengbaocheng
Date: 2025-02-24 11:28:16
LastEditors: zengbaocheng
LastEditTime: 2025-02-24 14:14:24
Desc: 
'''
import asyncio
import json
import uuid
import six
import websockets


class RpcServer:
    def __init__(self, port=5101):
        self.port = port

    def __call__(self, rpc_func):
        self.rpc_func = rpc_func
        return self.run_server

    async def handle_client(self, websocket):
        try:
            await self.rpc_func(websocket)  # 执行被装饰的RPC方法
            async for message in websocket:
                print(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")

    def run_server(self):
        async def start_server():
            async with websockets.serve(self.handle_client, "localhost", self.port):
                print(f"Server started at ws://localhost:{self.port}")
                await asyncio.Future()

        asyncio.run(start_server())


async def sleep(t):
    await asyncio.sleep(t)  # 异步等待


def format_request(func, *args, **kwargs):
    rid = six.text_type(uuid.uuid4())
    payload = {
        "method": func,
        "params": args or kwargs or [],
        "jsonrpc": "2.0",
        "id": rid,
    }
    req = json.dumps(payload)
    return req


# 使用类装饰器定义RPC服务
@RpcServer(port=5101)
async def main(websocket):
    request = format_request("test", [1, 2], {"a": 1, "b": 2})
    await websocket.send(request)
    print('发送request = format_request("test", [1, 2], {"a": 1, "b": 2})')
    response1 = await websocket.recv()
    print("第一次响应:", response1)

    await sleep(2)  # 异步等待

    request = format_request("getScreenSize")
    await websocket.send(request)
    print('发送request = format_request("getScreenSize")')
    response2 = await websocket.recv()
    print("第二次响应:", response2)

if __name__ == "__main__":
    main()  # 直接运行main()即可启动服务器