'''
Author: zengbaocheng
Date: 2025-02-22 10:58:57
LastEditors: zengbaocheng
LastEditTime: 2025-02-22 10:59:11
Desc: 
'''

from poco.agent import PocoAgent
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.ws import WebSocketClient

# __all__ = ['CocosTsPoco']
DEFAULT_PORT = 5003
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)

class CocosTsPocoAgent(PocoAgent):
    def __init__(self, port, device=None, ip=None):
        # transport
        self.conn = WebSocketClient('ws://{}:{}'.format(ip, port))
        self.c = RpcClient(self.conn)
        self.c.connect()
