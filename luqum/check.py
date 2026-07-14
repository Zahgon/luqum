# -*- coding: utf-8 -*-
import functools
import math
import re

from . import tree
from . import visitor
from .exceptions import NestedSearchFieldException, ObjectSearchFieldException
from .utils import flatten_nested_fields_specs, normalize_object_fields_specs


def camel_to_lower(name):
    return "".join(
        "_" + w.lower() if w.isupper() else w.lower()
        for w in name).lstrip("_")


sign = functools.partial(math.copysign, 1)


def _check_children(f):
    pass


class LuceneCheck:
    field_name_re = re.compile(r"^\w+$")
    space_re = re.compile(r"\s")
    invalid_term_chars_re = re.compile(r"[+/-]")

    SIMPLE_EXPR_FIELDS = (
        tree.Boost, tree.Proximity, tree.Fuzzy, tree.Word, tree.Phrase)

    FIELD_EXPR_FIELDS = tuple(list(SIMPLE_EXPR_FIELDS) + [tree.FieldGroup])

    def __init__(self, zeal=0):
        self.zeal = zeal

    def _check_field_name(self, fname):
        pass

    @_check_children
    def check_search_field(self, item, parents):
        pass

    @_check_children
    def check_group(self, item, parents):
        pass

    @_check_children
    def check_field_group(self, item, parents):
        pass

    def check_range(self, item, parents):
        pass

    def check_word(self, item, parents):
        pass

    def check_fuzzy(self, item, parents):
        pass

    def check_proximity(self, item, parents):
        pass

    @_check_children
    def check_boost(self, item, parents):
        pass

    @_check_children
    def check_base_operation(self, item, parents):
        pass

    @_check_children
    def check_plus(self, item, parents):
        pass

    def _check_not_operator(self, item, parents):
        pass

    @_check_children
    def check_not(self, item, parents):
        pass

    @_check_children
    def check_prohibit(self, item, parents):
        pass

    def check(self, item, parents=[]):
        pass

    def __call__(self, tree):
        """return True only if there are no error
        """
        for error in self.check(tree):
            return False
        return True

    def errors(self, tree):
        pass


class CheckNestedFields(visitor.TreeVisitor):

    def __init__(self, nested_fields, object_fields=None, sub_fields=None):
        assert isinstance(nested_fields, dict)
        self.object_fields = normalize_object_fields_specs(object_fields)
        self.object_prefixes = set(k.rsplit(".", 1)[0] for k in self.object_fields or [])
        self.nested_fields = flatten_nested_fields_specs(nested_fields)
        self.nested_prefixes = set(k.rsplit(".", 1)[0] for k in self.nested_fields)
        self.sub_fields = normalize_object_fields_specs(sub_fields)
        super().__init__(track_parents=True)

    def visit_search_field(self, node, context):
        pass

    def _check_final_operation(self, node, context):
        pass

    def visit_phrase(self, node, context):
        pass

    def visit_term(self, node, context):
        pass

    def __call__(self, tree):
        return list(self.visit_iter(tree, context={"prefix": []}))
