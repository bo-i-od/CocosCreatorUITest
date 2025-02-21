
import re
from .exceptions import NoSuchComparatorException

__all__ = ['IMatcher', 'DefaultMatcher', 'EqualizationComparator', 'RegexpComparator']

class IMatcher(object):
    def match(self, cond, node):
        """
        测试节点是否符合给定条件。
        Args：
        cond（：obj：“tuple”）：查询表达式
        node（：py:class:`继承自AbstractNode<poco.sdk.AbstractNode>`）：要测试的节点
        Returns：
        bool：如果匹配则为True，否则为False。
        """
        raise NotImplementedError
    
class EqualizationComparator(object):
    """
    使用原生等价（==）比较运算符比较两个对象
    """
    def compare(self, l, r):
        return l == r
    
class RegexpComparator(object):
    """
    使用正则表达式比较两个对象。仅当原始值为字符串类型时可用。它总是
    如果原始值或给定模式不是：obj：`str`类型，则返回False。
    """
    def compare(self, origin, pattern):
        """
        Args：
            origin（：obj：`str`）：原始字符串
            pattern（：obj:`str`）：正则表达式模式字符串
        Returns：
            bool：如果匹配则为True，否则为False。
        """
        if origin is None or pattern is None:
            return False
        return re.match(pattern, origin) is not None
    
class DefaultMatcher(IMatcher):
    """
    poco层次遍历的默认匹配器实现。包括逻辑查询条件和谓词
    表达。在遍历层次树时，匹配器将在树的每个节点上应用匹配方法。

    不太好翻译，不如直接看原文和代码
    The formal definition of query condition as follows::

        expr := (op0, (expr0, expr1, ...))  
        expr := (op1, (arg1, arg2))  

    - ``op0``:obj:`str` is logical operator ('or' or 'and') which has the same semantics as in python, e.g. 'or'
      means this expression/condition matches if any of the exprN matches
    - ``op1``:obj:`str` is comparator, can be one of as follows::

        op1 := 'attr='
        op1 := 'attr.*='
        op1 := ... (other customized)

      - ``attr=`` corresponds to :py:class:`EqualizationComparator <poco.sdk.DefaultMatcher.EqualizationComparator>`.
      - ``attr.*=`` corresponds to :py:class:`RegexpComparator <poco.sdk.DefaultMatcher.RegexpComparator>`.
      
      The ``op1`` must be a string. The ``Matcher`` will help to map to ``Comparator`` object.
    """
    def __init__(self):
        super(DefaultMatcher, self).__init__()
        self.comparators = {
            'attr=': EqualizationComparator(),
            'attr.*=': RegexpComparator(),
        }

    def match(self, cond, node):
        """
        See Also: :py:meth:`IMatcher.match <poco.sdk.DefaultMatcher.IMatcher.match>`
        """

        op, args = cond

        # 条件匹配
        if op == 'and':
            for arg in args:
                if not self.match(arg, node):
                    return False
            return True

        if op == 'or':
            for arg in args:
                if self.match(arg, node):
                    return True
            return False

        # 属性匹配
        comparator = self.comparators.get(op)
        if comparator:
            attribute, value = args
            targetValue = node.getAttr(attribute)
            return comparator.compare(targetValue, value)

        raise NoSuchComparatorException(op, 'poco.sdk.DefaultMatcher')