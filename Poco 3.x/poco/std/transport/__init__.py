'''
Author: zengbaocheng
Date: 2025-02-21 17:37:11
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 17:37:22
Desc: 
'''
# coding=utf-8

class Transport(object):
    # 用于更新传输的状态，例如检查是否有新的数据到达、处理超时等情况
    def update(self, timeout=None):
        raise NotImplementedError
    # 用于向指定的目标发送数据
    def send(self, cid, data):
        raise NotImplementedError
    # 用于接收数据
    def recv(self):
        raise NotImplementedError
    # 用于建立与指定端点的连接
    def connect(self, endpoint):
        raise NotImplementedError
    # 用于断开与指定端点的连接
    def disconnect(self, endpoint=None):
        raise NotImplementedError
    # 用于将传输绑定到指定的端点，通常用于服务器端监听连接
    def bind(self, endpoint):
        raise NotImplementedError