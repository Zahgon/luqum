# -*- coding: utf-8 -*-
import re
from decimal import Decimal

_MARKER = object()


class Item(object):


    _equality_attrs = []
    _children_attrs = []

    def __init__(self, pos=None, size=None, head="", tail=""):
        self.pos = pos
        self.size = size
        self.head = head
        self.tail = tail

    def clone_item(self, **kwargs):
        pass

    def _clone_item(self, cls, *args, **kwargs):
        pass

    @property
    def children(self):
        pass

    @children.setter
    def children(self, value):
        pass

    def _head_tail(self, value, head_tail):
        pass

    def span(self, head_tail=False):
        """return (start, end) position of this element in global expression.

        :param bool head_tail: should span include head and tail of element ?
        """
        if self.pos is None:
            start, end = None, None
        else:
            start = self.pos - (len(self.head) if head_tail else 0)
            end = self.pos + self.size + (len(self.tail) if head_tail else 0)
        return start, end

    def __repr__(self):
        children = ", ".join(c.__repr__() for c in self.children)
        return "%s(%s)" % (self.__class__.__name__, children)

    def __eq__(self, other):
        """a generic equal operation

        It make uses of :py:attr:`Item._equality_attrs`,
        and also recursively compare children
        """
        return (
            self is other  # shortcut
        ) or (
            self.__class__ == other.__class__ and
            len(self.children) == len(other.children) and
            all(getattr(self, a, _MARKER) == getattr(other, a, _MARKER)
                for a in self._equality_attrs) and
            all(c.__eq__(d) for c, d in zip(self.children, other.children))
        )


class NoneItem(Item):

    def __str__(self, head_tail=False):
        return ""


NONE_ITEM = NoneItem()


class SearchField(Item):
    _equality_attrs = ['name']
    _children_attrs = ["expr"]

    def __init__(self, name, expr, **kwargs):
        self.name = name
        self.expr = expr
        super().__init__(**kwargs)

    def __str__(self, head_tail=False):
        value = self.name + ":" + self.expr.__str__(head_tail=True)
        return self._head_tail(value, head_tail)

    def __repr__(self):
        return "SearchField(%r, %s)" % (self.name, self.expr.__repr__())


class BaseGroup(Item):
    _children_attrs = ["expr"]

    def __init__(self, expr, **kwargs):
        self.expr = expr
        super().__init__(**kwargs)

    def __str__(self, head_tail=False):
        value = "(%s)" % self.expr.__str__(head_tail=True)
        return self._head_tail(value, head_tail)


class Group(BaseGroup):
    pass


class FieldGroup(BaseGroup):
    pass


def group_to_fieldgroup(g):
    pass


class Range(Item):

    LOW_CHAR = {True: '[', False: '{'}
    HIGH_CHAR = {True: ']', False: '}'}

    _equality_attrs = ['include_high', 'include_low']
    _children_attrs = ["low", "high"]

    def __init__(self, low, high, include_low=True, include_high=True, **kwargs):
        self.low = low
        self.high = high
        self.include_low = include_low
        self.include_high = include_high
        super().__init__(**kwargs)

    def __str__(self, head_tail=False):
        value = "%s%sTO%s%s" % (
            self.LOW_CHAR[self.include_low],
            self.low.__str__(head_tail=True),
            self.high.__str__(head_tail=True),
            self.HIGH_CHAR[self.include_high])
        return self._head_tail(value, head_tail)


class Term(Item):
    WILDCARDS_PATTERN = re.compile(r"((?<=[^\\])[?*]|\\\\[?*]|^[?*])")  # non escaped * and ?
    WORD_ESCAPED_CHARS = re.compile(r'\\(.)')

    _equality_attrs = ['value']

    def __init__(self, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)

    @property
    def unescaped_value(self):
        pass

    def is_wildcard(self):
        pass

    def iter_wildcards(self):
        """list wildcards contained in value and their positions
        """
        for matched in self.WILDCARDS_PATTERN.finditer(self.value):
            yield matched.span(), matched.group()

    def split_wildcards(self):
        pass

    def has_wildcard(self):
        """:return bool: True if value contains a wildcards
        """
        return any(self.iter_wildcards())

    def __str__(self, head_tail=False):
        value = self.value
        return self._head_tail(value, head_tail)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self))


class Word(Term):
    pass


class Phrase(Term):
    def __init__(self, value, **kwargs):
        super(Phrase, self).__init__(value, **kwargs)
        assert self.value.endswith('"') and self.value.startswith('"'), (
               "Phrase value must contain the quotes")


class Regex(Term):
    def __init__(self, value, **kwargs):
        super(Regex, self).__init__(value, **kwargs)
        assert value.endswith('/') and value.startswith('/'), (
               "Regex value must contain the slashes")


class BaseApprox(Item):
    _equality_attrs = ['degree']
    _children_attrs = ["term"]

    def __init__(self, term, degree=None, **kwargs):
        self.term = term
        self._implicit_degree = degree is None  # this is just for display
        self.degree = self._normalize_degree(degree)
        super().__init__(**kwargs)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.term.__repr__(), self.degree)

    def __str__(self, head_tail=False):
        value = "%s~%s" % (
            self.term.__str__(head_tail=True),
            self.degree if not self._implicit_degree else "",
        )
        return self._head_tail(value, head_tail)


class Fuzzy(BaseApprox):
    def _normalize_degree(self, degree):
        pass


class Proximity(BaseApprox):

    def _normalize_degree(self, degree):
        pass


class Boost(Item):
    _equality_attrs = ['force']
    _children_attrs = ["expr"]

    def __init__(self, expr, force, **kwargs):
        self.expr = expr
        self.force = Decimal(force).normalize() if force is not None else 1
        self.implicit_force = force is None
        super().__init__(**kwargs)

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.expr.__repr__(), self.force)

    def __str__(self, head_tail=False):
        force = "" if self.implicit_force else self.force
        value = "%s^%s" % (self.expr.__str__(head_tail=True), force)
        return self._head_tail(value, head_tail)


class BaseOperation(Item):

    def __init__(self, *operands, **kwargs):
        self.operands = operands
        super().__init__(**kwargs)

    def __str__(self, head_tail=False):
        value = ("%s" % self.op).join(o.__str__(head_tail=True) for o in self.operands)
        return self._head_tail(value, head_tail)

    @property
    def children(self):
        pass

    @children.setter
    def children(self, value):
        pass


class BoolOperation(BaseOperation):
    op = ""


class UnknownOperation(BaseOperation):
    op = ''


class OrOperation(BaseOperation):
    op = 'OR'


class AndOperation(BaseOperation):
    op = 'AND'


def create_operation(cls, a, b, op_tail=" "):
    pass


class Unary(Item):
    _children_attrs = ["a"]

    def __init__(self, a, **kwargs):
        self.a = a
        super().__init__(**kwargs)

    def __str__(self, head_tail=False):
        value = "%s%s" % (self.op, self.a.__str__(head_tail=True))
        return self._head_tail(value, head_tail)


class UnaryOperator(Unary):
    pass


class Plus(UnaryOperator):
    op = "+"


class Not(UnaryOperator):
    op = 'NOT'


class Prohibit(UnaryOperator):
    op = "-"


class OpenRange(Unary):

    _char = {True: '=', False: ''}
    _equality_attrs = ['include']

    def __init__(self, a, include=True, **kwargs):
        self.include = include
        super().__init__(a, **kwargs)

    def __str__(self, head_tail=False):
        value = "%s%s%s" % (self.op, self._char[self.include], self.a.__str__(head_tail=True))
        return self._head_tail(value, head_tail)


class From(OpenRange):
    op = ">"


class To(OpenRange):
    op = "<"
