'''
Author: zengbaocheng
Date: 2025-02-21 17:57:28
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 18:10:07
Desc: 
'''
import traceback
import uuid

# 当请求的方法不存在时，抛出该异常，包含请求的方法名和可用的方法列表。
class NoSuchMethod(Exception):
    def __init__(self, name, available_methods):
        msg = 'No such method "{}". Available methods {}'.format(name, available_methods)
        super(NoSuchMethod, self).__init__(msg)


class StdRpcReactor(object):
    def __init__(self):
        super(StdRpcReactor, self).__init__()
        self.slots = {}  # method name -> method 用于存储已注册的方法，键为方法名，值为对应的可调用对象。
        self.pending_response = {}  # rid -> result 用于存储待处理的响应，键为请求 ID，值为响应结果。

    """
    该方法用于注册一个方法，将方法名和对应的可调用对象存储到 self.slots 中。
    检查传入的 method 是否为可调用对象，如果不是则抛出 ValueError 异常。
    检查方法名是否已经存在，如果存在则抛出 ValueError 异常。
    """
    def register(self, name, method):
        if not callable(method):
            raise ValueError('Argument `method` should be a callable object. Got {}'.format(repr(method)))
        if name in self.slots:
            raise ValueError('"{}" already registered. {}'.format(name, repr(self.slots[name])))

        self.slots[name] = method
    
    """
    该方法用于根据方法名调用对应的方法。
    从 self.slots 中获取方法，如果方法不存在则抛出 NoSuchMethod 异常。
    调用方法并返回结果。
    """
    def dispatch(self, name, *args, **kwargs):
        method = self.slots.get(name)
        if not method:
            raise NoSuchMethod(name, self.slots.keys())

        return method(*args, **kwargs)
    
    """
    该方法用于处理 JSON-RPC 请求。
    构建一个响应字典，包含请求的 ID 和 JSON-RPC 版本。
    从请求中获取方法名和参数，调用 dispatch 方法执行方法。
    如果执行成功，将结果添加到响应字典的 result 字段中；如果发生异常，将异常信息和堆栈跟踪信息添加到响应字典的 error 字段中。
    """
    def handle_request(self, req):
        ret = {
            'id': req['id'],
            'jsonrpc': req['jsonrpc'],
        }

        method = req['method']
        params = req['params']
        try:
            result = self.dispatch(method, *params)
            ret['result'] = result
        except Exception as e:
            ret['error'] = {
                'message': '{}\n\n|--- REMOTE TRACEBACK ---|\n{}|--- REMOTE TRACEBACK END ---|'
                           .format(six.text_type(e), traceback.format_exc())
            }

        return ret
    
    """
    该方法用于处理 JSON-RPC 响应，将响应结果存储到 self.pending_response 中。
    """
    def handle_response(self, res):
        id = res['id']
        self.pending_response[id] = res

    """
    该方法用于构建一个 JSON-RPC 请求。
    生成一个唯一的请求 ID，构建请求字典，包含请求 ID、JSON-RPC 版本、方法名和参数。
    将请求 ID 添加到 self.pending_response 中，初始值为 None。
    """
    def build_request(self, method, *args, **kwargs):
        rid = uuid.uuid4()
        ret = {
            'id': rid,
            'jsonrpc': '2.0',
            'method': method,
            'params': args or kwargs or [],
        }
        self.pending_response[rid] = None
        return ret
    
    # 该方法用于根据请求 ID 获取响应结果。
    def get_result(self, rid):
        return self.pending_response.get(rid)