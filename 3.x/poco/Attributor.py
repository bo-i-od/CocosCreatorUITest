'''
Author: zengbaocheng
Date: 2025-02-21 15:01:56
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 15:05:40
Desc: 
'''

__all__ = ['Attributor']

class Attributor(object):
    """
    这是一个用于访问节点属性的辅助类。在某些情况下，无法显式调用节点成员函数，因此引入了以下两个函数。
    此类的实例将用于实现：py:class:`HierarchyInterface\
    <poco.sdk.interfaces.hierarchy。HierarchyInterface>`。 
    ..注意：不要在测试代码中显式调用这些方法。
    """
    def getAttr(self, node, attrName):
        if type(node) in (list, tuple):
            node_ = node[0]
        else:
            node_ = node
        return node_.getAttr(attrName)

    def setAttr(self, node, attrName, attrVal):
        if type(node) in (list, tuple):
            node_ = node[0]
        else:
            node_ = node
        node_.setAttr(attrName, attrVal)