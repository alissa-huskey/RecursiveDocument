# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
RecursiveDocument formats, in a console-friendly and human-readable way, a document specified through its structure (sections, sub-sections, paragraphs, etc.).

It is especially well suited for printing help messages for command-line executables.

For example::

    from RecursiveDocument import Document, Section, Paragraph

    doc = Document()
    section = Section("Section title")
    doc.add(section)
    section.add(Paragraph("Some text"))
    print doc.format()

will produce::

    Section title:
      Some text

Sections and sub-sections are indented by 2 spaces to improve readability.

When the contents of the document are large, they are wrapped to 70 caracters.

Because ``add`` returns ``self``, RecursiveDocument allows chaining of calls to ``add``::

    from RecursiveDocument import Document, Section, Paragraph

    print Document().add(
        Section("Section title")
        .add(Paragraph("Some text"))
        .add(Paragraph("Some other text"))
    ).format()

will produce::

    Section title:
      Some text

      Some other text
"""

import textwrap
import itertools


def _wrap(text, prefixLength):
    indent = prefixLength * " "
    return textwrap.wrap(text, initial_indent=indent, subsequent_indent=indent)


def _insertWhiteLines(blocks):
    hasPreviousBlock = False
    for block in blocks:
        firstLineOfBlock = True
        for line in block:
            if firstLineOfBlock and hasPreviousBlock:
                yield ""
            yield line
            firstLineOfBlock = False
            hasPreviousBlock = True


class Container:
    def __init__(self):
        self.__contents = []

    def add(self, content):
        """
        Appends content to this object. ``content`` can be ``None``, or any class from :mod:`RecursiveDocument` but :class:`Document`.

        Returns self to allow chaining.
        """
        if content is not None:
            self.__contents.append(content)
        return self

    def _formatContents(self, prefixLength):
        return _insertWhiteLines(c._format(prefixLength) for c in self.__contents)

    def _format(self, prefixLength):
        return self._formatContents(prefixLength)


class Document(Container):
    """
    The top-level document.
    """

    def format(self):
        """
        Formats the document and returns the generated string.
        """
        return "\n".join(self._formatContents(0)) + "\n"


class Section(Container):
    """
    A section in a document. Sections can be nested.
    """

    def __init__(self, title):
        Container.__init__(self)
        self.__title = title

    def _format(self, prefixLength):
        return itertools.chain(_wrap(self.__title + ":", prefixLength), self._formatContents(prefixLength + 2))


class Paragraph:
    """
    A paragraph in a document.
    """

    def __init__(self, text):
        self.__text = text

    def _format(self, prefixLength):
        return _wrap(self.__text, prefixLength)


class DefinitionList:
    """
    A list of terms with their definitions.

    Example::

        from RecursiveDocument import Document, Section, DefinitionList

        doc = Document()
        section = Section("Section title")
        doc.add(section)
        section.add(
            DefinitionList()
            .add("Item", Paragraph("Definition 1"))
            .add("Other item", Paragraph("Definition 2"))
        )
        print doc.format()

    will produce::

        Section title:
          Item        Definition 1
          Other item  Definition 2
    """

    __maxDefinitionPrefixLength = 24

    def __init__(self):
        self.__items = []

    def add(self, name, definition):
        """
        Appends a new term to the list.

        Return self to allow chaining.
        """
        self.__items.append((name, definition))
        return self

    def _format(self, prefixLength):
        definitionPrefixLength = 2 + max(
            itertools.chain(
                [prefixLength],
                (
                    len(prefixedName)
                    for prefixedName, definition, shortEnough in self.__prefixedItems(prefixLength)
                    if shortEnough
                )
            )
        )
        return itertools.chain.from_iterable(
            self.__formatItem(item, definitionPrefixLength)
            for item in self.__prefixedItems(prefixLength)
        )

    def __prefixedItems(self, prefixLength):
        for name, definition in self.__items:
            prefixedName = prefixLength * " " + name
            shortEnough = len(prefixedName) <= self.__maxDefinitionPrefixLength
            yield prefixedName, definition, shortEnough

    def __formatItem(self, item, definitionPrefixLength):
        prefixedName, definition, shortEnough = item
        subsequentIndent = definitionPrefixLength * " "

        # nameMustBeOnItsOwnLine = len(definition) == 0 or not shortEnough
        nameMustBeOnItsOwnLine = not shortEnough

        if nameMustBeOnItsOwnLine:
            yield prefixedName
            initialIndent = subsequentIndent
        else:
            initialIndent = prefixedName + (definitionPrefixLength - len(prefixedName)) * " "

        foo = True
        for line in definition._format(definitionPrefixLength):
            if foo:
                foo = False
                if not nameMustBeOnItsOwnLine:
                    line = prefixedName + line[len(prefixedName):]
            yield line
        if foo:
            yield prefixedName
