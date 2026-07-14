import warnings

from luqum.elasticsearch.tree import ElasticSearchItemFactory
from luqum.exceptions import OrAndAndOnSameLevel
from luqum.tree import OrOperation, AndOperation, UnknownOperation
from luqum.tree import Word  # noqa: F401
from .tree import (
    EMust, EMustNot, EShould, EWord, EPhrase, ERange,
    ENested, EBoolOperation)
from ..check import CheckNestedFields
from ..naming import get_name
from ..utils import (
    normalize_nested_fields_specs, normalize_object_fields_specs, flatten_nested_fields_specs)
from ..visitor import TreeVisitor


class ElasticsearchQueryBuilder(TreeVisitor):

    SHOULD = 'should'
    MUST = 'must'

    CONTEXT_ANALYZE_MARKER = "analyzed"
    CONTEXT_FIELD_PREFIX = "field_prefix"

    E_MUST = EMust
    E_MUST_NOT = EMustNot
    E_SHOULD = EShould
    E_WORD = EWord
    E_PHRASE = EPhrase
    E_RANGE = ERange
    E_NESTED = ENested
    E_BOOL_OPERATION = EBoolOperation

    def __init__(self, default_operator=SHOULD, default_field='text',
                 not_analyzed_fields=None, nested_fields=None, object_fields=None, sub_fields=None,
                 field_options=None, match_word_as_phrase=False):
        """
        :param default_operator: to replace blank operator (MUST or SHOULD)
        :param default_field: to search
        :param not_analyzed_fields: field that are not analyzed in ES
          (do not forget to include eventual sub fields)
        :param nested_fields: dict contains fields that are nested in ES
            each nested fields contains
            either a dict of nested fields
            (if some of them are also nested)
            or a list of nesdted fields (this is for commodity)

            exemple, a where record contains multiple authors,
            each with one name and multiple books.
            Each book has on title but multiple formats with on type each::

                'author': {
                    'name': None,
                    'book': {
                        'format': ['type'],
                        'title': None
                    }
                },
        :param object_fields: list containing full qualified names of object fields.
          You may also use a spec similar to the one used for nested_fields.
          None, will accept all non nested fields as object fields.
        :param sub_fields: list containing full qualified names of sub fields.
          None, will accept all non nested fields or object fields as sub fields.
        :param dict field_options: allows you to give defaults options for each fields.
          They will be applied unless, overwritten by generated parameters.
          For match query, the `match_type` parameter modifies the type of match query.
        :param bool match_word_as_phrase: if True,
          word expressions are matched using `match_phrase` instead of `match`.
          This options mainly keeps stability with 0.6 version.
          It may be removed in the future.

        .. note::
            some of the parameters above
            can be deduced from elasticsearch index configuration.
            see :py:meth:`luqum.elasticsearch.schema.SchemaAnalyzer.query_builder_options`

        """
        super().__init__(track_parents=True)
        if not_analyzed_fields:
            self._not_analyzed_fields = not_analyzed_fields
        else:
            self._not_analyzed_fields = []

        self.nested_fields = self._normalize_nested_fields(nested_fields)
        self._nested_prefixes = set(
            k.rsplit(".", 1)[0]
            for k in flatten_nested_fields_specs(self.nested_fields))
        self.object_fields = self._normalize_object_fields(object_fields)
        self.sub_fields = sub_fields
        self.field_options = field_options or {}
        self.default_operator = default_operator
        self.default_field = default_field
        self.es_item_factory = ElasticSearchItemFactory(
            no_analyze=self._not_analyzed_fields,
            nested_fields=self.nested_fields,
            field_options=self.field_options,
        )
        self.nesting_checker = CheckNestedFields(
            nested_fields=self.nested_fields,
            object_fields=self.object_fields,
            sub_fields=self.sub_fields,
        )
        if match_word_as_phrase:
            warnings.warn(
                "match_word_as_phrase is a transient option " +
                "to keep compatibility with previous versions.\n" +
                "Consider wrapping your expressions in quotes (maybe using a transformer) " +
                "or forcing type in field_options.",
                PendingDeprecationWarning)
        self.match_word_as_phrase = match_word_as_phrase

    def _field_prefix(self, context):
        pass

    def _fields(self, context):
        pass

    def _split_nested(self, node, context):
        pass

    def _is_analyzed(self, context):
        """return if current search field is analyzed
        """
        marker = context.get(self.CONTEXT_ANALYZE_MARKER) if context is not None else None
        if marker is None:
            return self.default_field not in self._not_analyzed_fields
        else:
            return marker

    def _normalize_nested_fields(self, nested_fields):
        pass

    def _normalize_object_fields(self, object_fields):
        pass

    def simplify_if_same(self, children, current_node):
        pass

    def _get_operator_extract(self, binary_operation, delta=8):
        pass

    def _is_must(self, operation):
        pass

    def _is_should(self, operation):
        pass

    def _propagate_name(self, node, child_context):
        pass

    def get_name(self, node, context):
        """get node name or take it from context (inherited from upper layers)
        """
        node_name = get_name(node)
        return node_name if node_name is not None else context.get("name")

    def _yield_nested_children(self, parent, children):
        pass

    def _binary_operation(self, cls, node, context):
        pass

    def _must_operation(self, *args, **kwargs):
        pass

    def _should_operation(self, *args, **kwargs):
        pass

    def visit_and_operation(self, *args, **kwargs):
        pass

    def visit_or_operation(self, *args, **kwargs):
        pass

    def visit_search_field(self, node, context):
        pass

    def visit_not(self, node, context):
        pass

    def visit_prohibit(self, *args, **kwargs):
        pass

    def visit_plus(self, *args, **kwargs):
        pass

    def visit_bool_operation(self, *args, **kwargs):
        pass

    def visit_unknown_operation(self, *args, **kwargs):
        pass

    def visit_boost(self, node, context):
        pass

    def visit_fuzzy(self, node, context):
        pass

    def visit_proximity(self, node, context):
        pass

    def generic_visit(self, node, context):
        pass

    def visit_word(self, node, context):
        pass

    def visit_phrase(self, node, context):
        pass

    def visit_range(self, node, context):
        pass

    def __call__(self, tree):
        """Calling the query builder returns
        you the json compatible structure corresponding to the request tree passed in parameter

        :param luqum.tree.Item tree: a luqum parse tree
        :return dict:
        """
        self.nesting_checker(tree)
        elastic_tree = self.visit(tree)
        return elastic_tree[0].json
