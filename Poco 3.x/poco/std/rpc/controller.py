'''
Author: zengbaocheng
Date: 2025-02-21 17:52:34
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 18:21:01
Desc: 
'''

"""
json：用于进行 JSON 数据的序列化和反序列化操作，因为 RPC 通信中通常使用 JSON 格式来传输数据。
time：用于在 call 方法中进行时间延迟操作。
"""
import json
import time

# 自定义异常类，用于在 RPC 调用过程中发生远程错误时抛出异常。
class RpcRemoteException(Exception):
    pass

class StdRpcEndpointController(object):
    """
    初始化方法：接收两个参数 transport 和 reactor。
    transport：负责数据的传输，例如通过网络发送和接收数据，它应该实现了 update、send 等方法。
    reactor：负责处理 RPC 请求和响应，例如根据请求调用相应的方法并返回结果。
    """
    def __init__(self, transport, reactor):
        super(StdRpcEndpointController, self).__init__()
        self.transport = transport
        self.reactor = reactor

    """
    deserialize：将接收到的二进制或文本数据反序列化为 Python 对象，在 Python 3 中，如果数据是二进制类型，会先将其解码为 UTF-8 字符串，然后使用 json.loads 进行反序列化。
    serialize：将 Python 对象序列化为 JSON 字符串，使用 json.dumps 方法。
    """
    def deserialize(self, data):
        return json.loads(data)
    
    def serialize(self, packet):
        return json.dumps(packet)
    
    """
    serve_forever：使服务永久运行，不断接收和处理 RPC 请求和响应。
    调用 self.transport.update() 方法更新传输状态并获取客户端 ID（cid）和数据。
    如果接收到数据，将其反序列化为 Python 对象。
    如果数据包中包含 method 字段，说明这是一个 RPC 请求，调用 self.reactor.handle_request 处理请求并得到结果，然后将结果序列化并发送回客户端。
    如果数据包中不包含 method 字段，说明这是一个 RPC 响应，调用 self.reactor.handle_response 处理响应。
    """
    def serve_forever(self):
        while True:
            cid, data = self.transport.update()
            if data:
                packet = self.deserialize(data)
                if 'method' in packet:
                    result = self.reactor.handle_request(packet)
                    sres = self.serialize(result)
                    self.transport.send(cid, sres)
                else:
                    self.reactor.handle_response(packet)

    """
    call：发起一个 RPC 调用。
    调用 self.reactor.build_request 构建一个 RPC 请求包，并获取请求 ID（rid）。
    将请求包序列化并通过 self.transport.send 方法发送出去。
    进入一个无限循环，每隔 4 毫秒检查一次是否收到对应的响应。
    如果收到响应，检查响应中是否包含 result 字段，如果包含则返回结果；如果包含 error 字段，则抛出 RpcRemoteException 异常；如果都不包含，则抛出 RuntimeError 异常。
    """
    def call(self, method, *args, **kwargs):
        req = self.reactor.build_request(method, *args, **kwargs)
        rid = req['id']
        sreq = self.serialize(req)
        self.transport.send(None, sreq)
        while True:
            time.sleep(0.004)
            res = self.reactor.get_result(rid)
            if res is not None:
                if 'result' in res:
                    return res['result']

                if 'error' in res:
                    raise RpcRemoteException(res['error']['message'])

                raise RuntimeError('Invalid response from {}. Got {}'.format(self.transport, res))