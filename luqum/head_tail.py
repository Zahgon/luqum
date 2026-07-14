from .tree import Item


class TokenValue:

    def __init__(self, value):
        self.value = value
        self.pos = None
        self.size = None
        self.head = ""
        self.tail = ""

    def __repr__(self):
        return "TokenValue(%s)" % self.value

    def __str__(self):
        return str(self.value) if self.value else ""


class HeadTailLexer:

    LEXER_ATTR = "_luqum_headtail"

    @classmethod
    def handle(cls, token, orig_value):
        pass

    def __init__(self):
        self.head = None
        """This will track the head of next element, useful only for first element
        """
        self.last_elt = None
        """This will track the last token, so we can use it to add the tail to it.
        """

    def handle_token(self, token, orig_value):
        pass


token_headtail = HeadTailLexer.handle


class HeadTailManager:

    def pos(self, p, head_transfer=False, tail_transfer=False):
        pass

    def binary_operation(self, p, op_tail):
        pass

    def simple_term(self, p):
        pass

    def unary(self, p):
        pass

    def post_unary(self, p):
        pass

    def paren(self, p):
        pass

    def range(self, p):
        pass

    def search_field(self, p):
        pass


head_tail = HeadTailManager()
"""singleton of HeadTailManager
"""
