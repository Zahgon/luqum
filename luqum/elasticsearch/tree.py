import abc
import re

from ..tree import Term


class JsonSerializableMixin:

    @property
    @abc.abstractmethod
    def json(self):
        pass  # pragma: no cover


class AbstractEItem(JsonSerializableMixin):

    boost = None
    _fuzzy = None

    _KEYS_TO_ADD = ('boost', 'fuzziness', '_name')
    ADDITIONAL_KEYS_TO_ADD = ()

    def __init__(self, no_analyze=None, method='term', fields=[], _name=None, field_options=None):
        self._method = method
        self._fields = fields
        self._no_analyze = no_analyze if no_analyze else []
        self.zero_terms_query = 'none'
        self.field_options = field_options or {}
        if _name is not None:
            self._name = _name

    @property
    def json(self):
        pass

    @property
    def field(self):
        pass

    @property
    def fuzziness(self):
        pass

    @fuzziness.setter
    def fuzziness(self, fuzzy):
        pass

    def _value_has_wildcard_char(self):
        term = Term(getattr(self, 'q', ''))
        return term.has_wildcard()

    def _is_analyzed(self):
        return self.field not in self._no_analyze

    @property
    def method(self):
        is_analyzed = self._is_analyzed()
        if not is_analyzed and self._value_has_wildcard_char():
            return 'wildcard'
        elif is_analyzed:
            if self._value_has_wildcard_char():
                return 'query_string'
            elif self._method.startswith("match"):
                options = self.field_options.get(self.field, {})
                return options.get("match_type", options.get("type", self._method))
        return self._method


class EWord(AbstractEItem):

    ADDITIONAL_KEYS_TO_ADD = ('q', )

    def __init__(self, q, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q

    @property
    def json(self):
        pass


class EPhrase(AbstractEItem):

    ADDITIONAL_KEYS_TO_ADD = ('q',)
    _proximity = None

    def __init__(self, phrase, *args, **kwargs):
        super().__init__(method='match_phrase', *args, **kwargs)
        phrase = self._replace_CR_and_LF_by_a_whitespace(phrase)
        self.q = self._remove_double_quotes(phrase)

    def __repr__(self):
        return "%s(%s=%s)" % (self.__class__.__name__, self.field, self.q)

    def _replace_CR_and_LF_by_a_whitespace(self, phrase):
        pass

    def _remove_double_quotes(self, phrase):
        pass

    def _value_has_wildcard_char(self):
        return False

    @property
    def slop(self):
        pass

    @slop.setter
    def slop(self, slop):
        pass


class ERange(AbstractEItem):

    def __init__(self, lt=None, lte=None, gt=None, gte=None, *args, **kwargs):
        super().__init__(method='range', *args, **kwargs)
        if lt and lt != '*':
            self.lt = lt
            self.ADDITIONAL_KEYS_TO_ADD += ('lt', )
        elif lte and lte != '*':
            self.lte = lte
            self.ADDITIONAL_KEYS_TO_ADD += ('lte', )
        if gt and gt != '*':
            self.gt = gt
            self.ADDITIONAL_KEYS_TO_ADD += ('gt', )
        elif gte and gte != '*':
            self.gte = gte
            self.ADDITIONAL_KEYS_TO_ADD += ('gte', )


class AbstractEOperation(JsonSerializableMixin):
    pass


class EOperation(AbstractEOperation):

    def __init__(self, items, **options):
        self.items = items
        self._method = None
        self.options = options

    def __repr__(self):
        items = ", ".join(i.__repr__() for i in self.items)
        return "%s(%s)" % (self.__class__.__name__, items)

    @property
    def json(self):
        pass


class ENested(AbstractEOperation):

    def __init__(self, nested_path, nested_fields, items, *args, _name=None, **kwargs):

        self._nested_path = [nested_path]
        self.items = self._exclude_nested_children(items)
        self._name = _name

    @property
    def nested_path(self):
        pass

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.nested_path, self.items)

    def _exclude_nested_children(self, subtree):
        pass

    @property
    def json(self):
        pass


class EShould(EOperation):
    operation = 'should'


class AbstractEMustOperation(EOperation):

    def __init__(self, items, **options):
        op = super().__init__(items, **options)
        for item in self.items:
            item.zero_terms_query = self.zero_terms_query
        return op


class EMust(AbstractEMustOperation):
    zero_terms_query = 'all'
    operation = 'must'


class EMustNot(AbstractEMustOperation):
    zero_terms_query = 'none'
    operation = 'must_not'


class EBoolOperation(EOperation):

    @property
    def json(self):
        pass


class ElasticSearchItemFactory:

    def __init__(self, no_analyze, nested_fields, field_options):
        self._no_analyze = no_analyze
        self._nested_fields = nested_fields
        self._nested_fields = nested_fields
        self._field_options = field_options

    def build(self, cls, *args, **kwargs):
        pass
