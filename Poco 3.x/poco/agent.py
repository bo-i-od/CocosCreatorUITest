'''
Author: zengbaocheng
Date: 2025-02-22 11:00:33
LastEditors: zengbaocheng
LastEditTime: 2025-02-22 11:01:51
Desc: 
'''

class PocoAgent(object):
    # 这是poco与目标设备通信的代理类

    def rpc_reconnect(self):
        self.rpc.close()
        self.rpc.connect()

    @property
    def rpc(self):
        """
        Return the interface of this agent handled.

        Returns:
            :py:obj:`object`: the rpc interface of this agent handled.

        Raises:
            NotImplementedError: raises if the agent implementation dose not expose the rpc interface to user.
        """

        raise NotImplementedError('This poco agent does not have a explicit rpc connection.')
