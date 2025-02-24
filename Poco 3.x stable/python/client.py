import asyncio
import json
import websockets


# 定义客户端可调用的函数
def client_function(a, b):
    return a * b


# 处理服务器请求
async def handle_server_request(websocket):
    while True:
        try:
            # 接收服务器消息
            message = await websocket.recv()
            try:
                # 解析 JSON 消息
                request = json.loads(message)
                method = request.get('method')
                params = request.get('params', [])
                request_id = request.get('id')

                if method == 'client_function':
                    result = client_function(*params)
                    # 构建响应消息
                    response = {
                        'id': request_id,
                        'result': result,
                        'error': None
                    }
                else:
                    response = {
                        'id': request_id,
                        'result': None,
                        'error': f'Unknown method: {method}'
                    }
                # 发送响应消息给服务器
                await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                # 处理 JSON 解析错误
                error_response = {
                    'id': None,
                    'result': None,
                    'error': 'Invalid JSON message'
                }
                await websocket.send(json.dumps(error_response))
        except websockets.exceptions.ConnectionClosedOK:
            break


# 连接到服务器
async def connect_to_server():
    uri = "ws://localhost:6666"
    async with websockets.connect(uri) as websocket:
        # 启动处理服务器请求的任务
        await handle_server_request(websocket)


if __name__ == "__main__":
    asyncio.run(connect_to_server())
