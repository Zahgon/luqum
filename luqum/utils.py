# -*- coding: utf-8 -*-
from . import visitor
from .deprecated_utils import (  # noqa: F401
    LuceneTreeTransformer, LuceneTreeVisitor, LuceneTreeVisitorV2)
from .tree import AndOperation, BaseOperation, OrOperation, BoolOperation, Range, Word


class UnknownOperationResolver(visitor.TreeTransformer):

    VALID_OPERATIONS = frozenset([None, AndOperation, OrOperation, BoolOperation])
    DEFAULT_OPERATION = AndOperation

    def __init__(self, resolve_to=None, add_head=" "):
        """Initialize a new resolver

        :param resolve_to: must be either None, OrOperation, AndOperation, BoolOperation.

          for the latter three the UnknownOperation is replaced by specified operation.

          if it is None, we use the last operation encountered, as would Lucene do
        """
        if resolve_to not in self.VALID_OPERATIONS:
            raise ValueError("%r is not a valid value for resolve_to" % resolve_to)
        self.resolve_to = resolve_to
        self.add_head = add_head
        super().__init__(track_parents=True)

    def _last_operation(self, context):
        pass

    def _first_nonop_parent(self, parents):
        pass

    def _track_last_op(self, node, context):
        pass

    def _get_last_op(self, node, context):
        pass

    def visit_or_operation(self, node, context):
        pass

    def visit_and_operation(self, node, context):
        pass

    def visit_unknown_operation(self, node, context):
        pass

    def __call__(self, tree):
        return self.visit(tree)


class OpenRangeTransformer(visitor.TreeTransformer):

    WILDCARD_WORD = Word("*")

    def __init__(self, merge_ranges=False, add_head=" "):
        self.merge_ranges = merge_ranges
        self.add_head = add_head
        super().__init__(track_parents=True)

    def _get_node_bound_side(self, node):
        pass

    def visit_and_operation(self, node, context):
        pass

    def _visit_from_to(self, node, context, bound_side):
        pass

    def visit_from(self, node, context):
        pass

    def visit_to(self, node, context):
        pass

    def __call__(self, tree):
        return self.visit(tree)


def normalize_nested_fields_specs(nested_fields):
    pass


def _flatten_fields_specs(object_fields):
    pass


def flatten_nested_fields_specs(nested_fields):
    pass


def normalize_object_fields_specs(object_fields):
    pass
