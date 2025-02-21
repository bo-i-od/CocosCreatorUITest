'''
Author: zengbaocheng
Date: 2025-02-21 14:28:11
LastEditors: zengbaocheng
LastEditTime: 2025-02-21 14:57:42
Desc: 
'''

# coding=utf-8

"""
此模块为poco-sdk提供了几个例外。这些异常仅在sdk对应的运行时中引发。
"""

__all__ = ['NoSuchTargetException', 'NodeHasBeenRemovedException', 'UnableToSetAttributeException',
           'NoSuchComparatorException', 'NonuniqueSurfaceException', 'InvalidSurfaceException']

class NodeHasBeenRemovedException(Exception):
    """
    在遍历层次结构期间检索属性时刷新（更新、回收或销毁）节点（UI元素）时引发。
    在某些引擎实现中，当poco执行遍历过程时，UI层次结构会在独立线程中刷新，
    因此当poco试图检索UI元素的属性但同时更新属性时，可能会触发引擎错误。在这种情况下，poco-sdk会抓住引擎
    错误并引发此异常。
    """
    def __init__(self, attrName, node):
        msg = 'Node was no longer alive when query attribute "{}". Please re-select.'.format(attrName)
        super(NodeHasBeenRemovedException, self).__init__(msg)

class UnableToSetAttributeException(Exception):
    """
    当设置给定UI元素的属性失败时引发。在大多数情况下，它失败的原因是
    UI元素不支持突变。从SDK实现的角度来看，这个异常可以是
    主动提出，表示不允许修改属性。
    """
    def __init__(self, attrName, node):
        msg = 'Unable to set attribute "{}" of node "{}".'.format(attrName, node)
        super(UnableToSetAttributeException, self).__init__(msg)

class NoSuchTargetException(Exception):
    """
    当索引超出给定索引选择UI元素的范围时引发。
    """
    pass

class NoSuchComparatorException(Exception):
    """
    当匹配器不支持给定的比较方法时引发。
    """
    def __init__(self, matchingMethod, matcherName):
        super(NoSuchComparatorException, self).__init__()
        self.message = 'No such matching method "{}" of this Matcher ("{}")'.format(matchingMethod, matcherName)

class NonuniqueSurfaceException(Exception):
    """
    当设备选择器匹配多个设备时引发
    """
    def __init__(self, selector):
        msg = 'The arguments ("{}") match multiple device surface. More precise conditions required.'.format(selector)
        super(NonuniqueSurfaceException, self).__init__(msg)

class InvalidSurfaceException(Exception):
    """
    当设备无效时引发
    """
    def __init__(self, target, msg="None"):
        msg = 'Target device surface invalid ("{}") . Detail message: "{}"'.format(target, msg)
        super(InvalidSurfaceException, self).__init__(msg)

