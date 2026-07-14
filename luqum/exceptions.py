class InconsistentQueryException(Exception):
    pass


class OrAndAndOnSameLevel(InconsistentQueryException):
    pass


class NestedSearchFieldException(InconsistentQueryException):
    pass


class ObjectSearchFieldException(InconsistentQueryException):
    pass


class ParseError(ValueError):
    pass


class ParseSyntaxError(ParseError):
    pass


class IllegalCharacterError(ParseError):
    pass
