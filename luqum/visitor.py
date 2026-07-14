# -*- coding: utf-8 -*-


def camel_to_lower(name):
    return "".join(
        "_" + w.lower() if w.isupper() else w.lower()
        for w in name).lstrip("_")


class TreeVisitor:
    visitor_method_prefix = 'visit_'
    generic_visitor_method_name = 'generic_visit'

    def __init__(self, track_parents=False):
        self.track_parents = track_parents

    _get_method_cache = None

    def _get_method(self, node):
        if self._get_method_cache is None:
            self._get_method_cache = {}
        try:
            meth = self._get_method_cache[type(node)]
        except KeyError:
            for cls in node.__class__.mro():
                try:
                    method_name = "{}{}".format(
                        self.visitor_method_prefix,
                        camel_to_lower(cls.__name__)
                    )
                    meth = getattr(self, method_name)
                    break
                except AttributeError:
                    continue
            else:
                meth = getattr(self, self.generic_visitor_method_name)
            self._get_method_cache[type(node)] = meth
        return meth

    def visit(self, tree, context=None):
        """Traversal of tree

        :param luqum.tree.Item tree: a tree representing a lucene expression
        :param dict context: a dict with initial values for context

        .. note:: the values in context, are not guaranteed to move up the hierachy,
           because we do copy of context for children to have specific values.

           A trick you can use if you need values to move up the hierachy
           is to set a `"global"` key containing a dict, where you can store values.
        """
        if context is None:
            context = {}
        return list(self.visit_iter(tree, context=context))

    def visit_iter(self, node, context):
        """
        Basic, recursive traversal of the tree.

        :param list parents: the list of parents
        :param dict context: a dict of contextual variable for free use
            to track states while traversing the tree (eg. the current field name)
        """
        method = self._get_method(node)
        yield from method(node, context)

    def child_context(self, node, child, context, **kwargs):
        pass

    def generic_visit(self, node, context):
        pass


class TreeTransformer(TreeVisitor):

    def __init__(self, track_new_parents=False, **kwargs):
        self.track_new_parents = track_new_parents
        super().__init__(**kwargs)

    def _clone_item(self, node):
        pass

    def visit(self, tree, context=None):
        """Visit the tree, by default building a copy and returning it.

        :param luqum.tree.Item tree: luqum expression tree
        :param context: optional initial context
        """
        if context is None:
            context = {}
        try:
            value, = self.visit_iter(tree, context=context)
            return value
        except ValueError as e:
            if str(e).startswith(("too many values to unpack", "not enough values to unpack")):
                exc = ValueError(
                    "The visit of the tree should have produced exactly one element "
                    "(the transformed tree)"
                )
                raise exc from e
            else:
                raise

    def child_context(self, node, child, context, **kwargs):
        pass

    def generic_visit(self, node, context):
        pass

    def clone_children(self, node, new_node, context):
        pass


class PathTrackingMixin:

    def child_context(self, node, child, context, **kwargs):
        pass

    def visit(self, node, context=None):
        """visit the tree while tracking their path
        """
        if context is None:
            context = {}
        context["path"] = ()
        return super().visit(node, context=context)


class PathTrackingVisitor(PathTrackingMixin, TreeVisitor):

    def generic_visit(self, node, context):
        pass


class PathTrackingTransformer(PathTrackingMixin, TreeTransformer):

    def clone_children(self, node, new_node, context):
        pass
