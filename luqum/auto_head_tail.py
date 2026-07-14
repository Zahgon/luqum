
from . import visitor


class AutoHeadTail(visitor.TreeTransformer):

    SPACER = " "

    def add_head(self, node):
        pass

    def add_tail(self, node):
        pass

    def visit_base_operation(self, node, context):
        pass

    def visit_unknown_operation(self, node, context):
        pass

    def visit_not(self, node, context):
        pass

    def visit_range(self, node, context):
        pass

    def __call__(self, tree):
        new_tree = self.visit(tree)
        return new_tree


auto_head_tail = AutoHeadTail()
"""method to auto add head and tail to items of a lucene tree so that it is printable
"""
