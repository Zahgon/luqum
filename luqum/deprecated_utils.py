
import warnings

from .visitor import camel_to_lower


class LuceneTreeVisitor:
    visitor_method_prefix = 'visit_'
    generic_visitor_method_name = 'generic_visit'

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

    def visit(self, node, parents=None):
        """ Basic, recursive traversal of the tree. """
        warnings.warn(
            "LuceneTreeVisitor is deprecated in favor of visitor.TreeVisitor",
            DeprecationWarning,
        )
        parents = parents or []
        method = self._get_method(node)
        yield from method(node, parents)
        for child in node.children:
            yield from self.visit(child, parents + [node])

    def generic_visit(self, node, parents=None):
        pass


class LuceneTreeTransformer(LuceneTreeVisitor):

    def replace_node(self, old_node, new_node, parent):
        for k, v in parent.__dict__.items():  # pragma: no branch
            if v == old_node:
                parent.__dict__[k] = new_node
                break
            elif isinstance(v, list):
                try:
                    i = v.index(old_node)
                    if new_node is None:
                        del v[i]
                    else:
                        v[i] = new_node
                    break
                except ValueError:
                    pass  # this was not the attribute containing old_node
            elif isinstance(v, tuple):
                try:
                    i = v.index(old_node)
                    v = list(v)
                    if new_node is None:
                        del v[i]
                    else:
                        v[i] = new_node
                    parent.__dict__[k] = tuple(v)
                    break
                except ValueError:
                    pass  # this was not the attribute containing old_node

    def generic_visit(self, node, parent=None):
        pass

    def visit(self, node, parents=None):
        """
        Recursively traverses the tree and replace nodes with the appropriate
        visitor method's return values.
        """
        warnings.warn(
            "LuceneTreeTransformer is deprecated in favor of visitor.TreeTransformer",
            DeprecationWarning,
        )
        parents = parents or []
        method = self._get_method(node)
        new_node = method(node, parents)
        if parents:
            self.replace_node(node, new_node, parents[-1])
        node = new_node
        if node is not None:
            for child in node.children:
                self.visit(child, parents + [node])
        return node


class LuceneTreeVisitorV2(LuceneTreeVisitor):

    def visit(self, node, parents=None, context=None):
        """ Basic, recursive traversal of the tree.

        :param list parents: the list of parents
        :parma dict context: a dict of contextual variable for free use
          to track states while traversing the tree
        """
        warnings.warn(
            "LuceneTreeVisitorV2 is deprecated in favor of visitor.TreeVisitor",
            DeprecationWarning,
        )
        if parents is None:
            parents = []

        method = self._get_method(node)
        return method(node, parents, context)

    def generic_visit(self, node, parents=None, context=None):
        """
        Default visitor function, called if nothing matches the current node.
        """
        raise AttributeError(
            "No visitor found for this type of node: {}".format(
                node.__class__
            )
        )
