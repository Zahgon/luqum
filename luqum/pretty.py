# -*- coding: utf-8 -*-
from .tree import BaseOperation, BaseGroup, SearchField


class _StickMarker:

    def __len__(self):
        return 0


_STICK_MARKER = _StickMarker()


class Prettifier(object):

    def __init__(self, indent=4, max_len=80, inline_ops=False):
        """
        The pretty printer factory.

        :param int indent: number of space for indentation
        :param int max_len: maximum line length in number of characters.
            Prettyfier will do its best to keep inside those margin,
            but as it can only split on operators, it may not be possible.
        :param bool inline_ops: if False (default) operators are printed on a new line
          if True, operators are printed at the end of the line.
        """
        self.indent = indent
        self.prefix = " " * self.indent
        self.max_len = max_len
        self.inline_ops = inline_ops

    def _get_chains(self, element, parent=None):
        pass

    def _count_chars(self, element):
        pass

    def _apply_stick(self, elements):
        pass

    def _concatenates(self, chain_with_counts, char_counts, level=0, in_one_liner=False):
        pass

    def __call__(self, tree):
        """Pretty print the query represented by tree

        :param tree: a query tree using elements from :py:mod:`luqum.tree`
        """
        chains = list(self._get_chains(tree))
        chain_with_counts, total = self._count_chars(chains)
        return self._concatenates(chain_with_counts, total)


prettify = Prettifier()
"""prettify function with default parameters
"""
