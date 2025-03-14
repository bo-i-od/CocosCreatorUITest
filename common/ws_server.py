import asyncio
import json
import uuid
import websockets
from colorama import Fore, Style, init
from common import rpc_method_request
init(autoreset=True)
COLOR_MAPPING = {
    'log': Style.RESET_ALL,
    'error': Fore.RED,
    'warn': Fore.YELLOW,
    'info': Fore.BLUE,
    'debug': Fore.CYAN
}


# 处理CocosCreator的console输出
# 目前是按照类型打印
def handle_msg(msg):
    msg_type = msg.get('type', 'log')
    data = msg.get('data', '')  # 默认空字符串而非列表

    # 获取对应颜色，默认为重置样式
    color = COLOR_MAPPING.get(msg_type, Style.RESET_ALL)

    # 处理整个数据字符串
    try:
        # 尝试解析为JSON（例如传输的是对象或数组）
        parsed = json.loads(data)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        # 否则直接使用原始字符串
        formatted = data

    # 打印带颜色的消息
    print(f"{color}[{msg_type.upper()}] {formatted}")


class RPCServer:
    def __init__(self, websocket):
        self.websocket = websocket
        self.pending_requests = {}
        self.listener_task = None

    async def _response_listener(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if 'id' not in data:
                    continue
                if 'msg' in data:
                    handle_msg(data.get('msg'))
                    continue
                rid = data['id']
                future = self.pending_requests.pop(rid, None)
                if not future:
                    continue
                if 'error' in data:
                    future.set_exception(Exception(data['error'].get('message', 'RPC Error')))
                    continue
                future.set_result(data.get('result'))
        except Exception as e:
            for future in self.pending_requests.values():
                future.set_exception(e)
            self.pending_requests.clear()

    async def call(self, method, *args, **kwargs):
        rid = str(uuid.uuid4())
        future = asyncio.Future()
        self.pending_requests[rid] = future

        request = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": args or kwargs,
            "id": rid
        })

        await self.websocket.send(request)
        return await future

    async def start(self):
        self.listener_task = asyncio.create_task(self._response_listener())

    async def close(self):
        if self.listener_task:
            self.listener_task.cancel()
            try:
                await self.listener_task
            except asyncio.CancelledError:
                pass
        await self.websocket.close()


def rpc_server(port=5101):
    def decorator(handler):
        async def wrapped_handler(websocket, stop_event):
            server = RPCServer(websocket)
            await server.start()
            try:
                await handler(server)
            finally:
                await server.close()
                stop_event.set()  # 触发服务器停止事件

        def run_server():
            async def server_main():
                stop_event = asyncio.Event()
                async with websockets.serve(lambda ws: wrapped_handler(ws, stop_event), "localhost", port):
                    print(f"RPC Server running at ws://localhost:{port}")
                    await stop_event.wait()  # 等待停止事件

            asyncio.run(server_main())

        return run_server

    return decorator


async def sleep(t):
    await asyncio.sleep(t)


@rpc_server(port=5101)
async def main(server):
    screen_size = await rpc_method_request.get_screen_size(server)
    print(f"Screen size: {screen_size}")
    await sleep(5)
    screen_size = await rpc_method_request.get_position(server, element_data_list=[])
    print(f"Screen size: {screen_size}")


if __name__ == "__main__":
    main()
