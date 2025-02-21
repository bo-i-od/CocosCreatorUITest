import asyncio
import json
import time
import traceback
import uuid

import websockets
from poco.utils.simplerpc.jsonrpc import six


def rpc_server(port=5101):
    """装饰器：用于启动WebSocket服务器并处理RPC连接"""

    def decorator(rpc_func):
        async def handle_client(websocket):
            try:
                await rpc_func(websocket)  # 执行被装饰的RPC方法
                async for message in websocket:
                    print(f"Received: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Client disconnected")

        def run_server():
            async def start_server():
                async with websockets.serve(handle_client, "localhost", port):
                    print(f"Server started at ws://localhost:{port}")
                    await asyncio.Future()

            asyncio.run(start_server())

        return run_server

    return decorator


async def sleep(t):
    await asyncio.sleep(t)  # 异步等待 5 秒

def format_request(func, *args, **kwargs):
    rid = six.text_type(uuid.uuid4())
    payload = {
        "method": func,
        "params": args or kwargs or [],
        "jsonrpc": "2.0",
        "id": rid,
    }
    # send rpc
    req = json.dumps(payload)

    # # init cb
    # cb = Callback(rid)
    return req



# 使用装饰器定义RPC服务
@rpc_server(port=5101)
async def main(websocket):
    request = format_request("getScreenSize")
    # response0 = await websocket.recv()
    # print(f'收到{response0}')
    await websocket.send(request)
    print('发送request = format_request("getScreenSize")')
    response1 = await websocket.recv()
    print("第一次响应:", response1)
    await sleep(2)  # 异步等待 5 秒
    await websocket.send(request)
    print('发送request = format_request("getScreenSize")')
    response2 = await websocket.recv()
    print("第二次响应:", response2)


if __name__ == "__main__":
    main()  # 直接运行rpc()即可启动服务器