from . import tree
from .visitor import PathTrackingVisitor, PathTrackingTransformer


NAME_ATTR = "_luqum_name"


def set_name(node, value):
    setattr(node, NAME_ATTR, value)


def get_name(node):
    return getattr(node, NAME_ATTR, None)


class TreeAutoNamer(PathTrackingVisitor):

    LETTERS = "abcdefghilklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _pos_letter = {l: i for i, l in enumerate(LETTERS)}

    def next_name(self, name):
        """Given name, return next name

        ::
           >>> tan = TreeAutoNamer()
           >>> tan.next_name(None)
           'a'
           >>> tan.next_name('aZ')
           'aZa'
           >>> tan.next_name('azb')
           'azc'
        """
        if name is None:
            return self.LETTERS[0]
        else:
            actual_pos = self._pos_letter[name[-1]]
            try:
                return name[:-1] + self.LETTERS[actual_pos + 1]
            except IndexError:
                return name + self.LETTERS[0]

    def visit_base_operation(self, node, context):
        pass

    def visit(self, node):
        """visit the tree and add names to nodes while tracking their path
        """
        context = {"global": {"name": None, "name_to_path": {}}}
        super().visit(node, context)
        name_to_path = context["global"]["name_to_path"]
        if not name_to_path:
            node_name = self.next_name(context["global"]["name"])
            set_name(node, node_name)
            name_to_path[node_name] = ()
        return name_to_path


def auto_name(tree, targets=None, all_names=False):
    """Automatically add names to nodes of a parse tree, in order to be able to track matching.

    We add them to top nodes under operations as this is where it is useful for ES named queries

    :return dict: association of name with the path (as a tuple) to a the corresponding children
    """
    return TreeAutoNamer().visit(tree)


def matching_from_names(names, name_to_path):
    """Utility to convert a list of name and the result of auto_name
    to the matching parameter for :py:class:`MatchingPropagator`

    :param list names: list of names
    :param dict name_to_path: association of names with path to children
    :return tuple: (set of matching paths, set of other known paths)
    """
    matching = {name_to_path[name] for name in names}
    return (matching, set(name_to_path.values()) - matching)


def element_from_path(tree, path):
    """Given a tree, retrieve element corresponding to path

    :param luqum.tree.Item tree: luqum expression tree
    :param tuple path: tuple representing top down access to a child
    :return  luqum.tree.Item: target item
    """
    node = tree
    path = list(path)
    while path:
        node = node.children[path.pop(0)]
    return node


def element_from_name(tree, name, name_to_path):
    return element_from_path(tree, name_to_path[name])


class MatchingPropagator:

    OR_NODES = (tree.OrOperation,)
    """A tuple of nodes types considered as OR operations
    """
    NEGATION_NODES = (tree.Not, tree.Prohibit)
    """A tuple of nodes types considered as NOT operations
    """
    NO_CHILDREN_PROPAGATE = (tree.Range, tree.BaseApprox)
    """A tuple of nodes for which propagation is of no use
    """

    def __init__(self, default_operation=tree.OrOperation):
        if default_operation is tree.OrOperation:
            self.OR_NODES = self.OR_NODES + (tree.UnknownOperation,)

    def _status_from_parent(self, path, matching, other):
        pass

    def _propagate(self, node, matching, other, path):
        pass

    def __call__(self, tree, matching, other=frozenset()):
        """
        Given a list of paths that are known to match,
        return all pathes in the tree that are matches.

        .. note:: we do not descend into nodes that are positive.
           Normally matching just provides nodes at the right levels
           for propagation to be effective.
           Descending would mean risking to give non consistent information.

        :param list matching: list of path of matching nodes (each path is a tuple)
        :param list other: list of other path that had a name, but were not reported as matching

        :return tuple: (
            set of matching path after propagation,
            set of non matching pathes after propagation)
        """
        tree_ok, paths_ok, paths_ko = self._propagate(tree, matching, other, ())
        return paths_ok, paths_ko


class ExpressionMarker(PathTrackingTransformer):

    def mark_node(self, node, path, *info):
        pass

    def generic_visit(self, node, context):
        pass

    def __call__(self, tree, *info):
        return self.visit(tree, context={"info": info})


class HTMLMarker(ExpressionMarker):

    def __init__(self, ok_class="ok", ko_class="ko", element="span"):
        super().__init__()
        self.ok_class = ok_class
        self.ko_class = ko_class
        self.element = element

    def css_class(self, path, paths_ok, paths_ko):
        pass

    def mark_node(self, node, path, paths_ok, paths_ko, parcimonious):
        pass

    def __call__(self, tree, paths_ok, paths_ko, parcimonious=True):
        """representation of tree, adding html elements with right class around subexpressions
        according to their presence in paths_ok or paths_ko

        :param tree: a luqum tree
        :param paths_ok: set of path to nodes (express as tuple of int) that should get ok_class
        :param paths_ko: set of path to nodes that should get ko_class
        :param parcimonious: only add class when parent node does not have same class

        :return str: expression with html elements surrounding part of expression
          with right class attribute according to paths_ok and paths_ko
        """
        new_tree = super().__call__(tree, paths_ok, paths_ko, parcimonious)
        return new_tree.__str__(head_tail=True)
