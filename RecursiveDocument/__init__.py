# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
Import:

    >>> from RecursiveDocument import Document, Section, Paragraph, DefinitionList

Create a simple document and format it:

    >>> doc = Document()
    >>> section = Section("Section title")
    >>> doc.add(section)
    <RecursiveDocument.Document ...>
    >>> section.add(Paragraph("Some text"))
    <RecursiveDocument.Section ...>
    >>> print doc.format()
    Section title
      Some text

Sections and sub-sections are indented by 2 spaces to improve readability.

When the contents of the document are large, they are wrapped to 70 caracters.

Because ``add`` returns ``self``, RecursiveDocument allows chaining of calls to ``add``::

    >>> print Document().add(
    ...   Section("Section title")
    ...   .add(Paragraph("Some text"))
    ...   .add(Paragraph("Some other text"))
    ... ).format()
    Section title
      Some text

      Some other text

Here is a more complex example:

    >>> lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus gravida."

    >>> doc = (Document()
    ...   .add(Paragraph(lorem))
    ...   .add(Paragraph(lorem))
    ...   .add(Section("Lorem is good")
    ...     .add(Paragraph(lorem))
    ...     .add(DefinitionList()
    ...       .add("foo", Paragraph("bar"))
    ...       .add("baz", Paragraph(lorem))
    ...     )
    ...     .add(Paragraph(lorem))
    ...   )
    ...   .add(Section("Lorem is life")
    ...     .add(Paragraph(lorem))
    ...     .add(Section("Lorem always").add(Paragraph(lorem)))
    ...   )
    ... )
    >>> print doc.format()
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida.
    <BLANKLINE>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida.
    <BLANKLINE>
    Lorem is good
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus
      gravida.
    <BLANKLINE>
      foo  bar
      baz  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
           Pellentesque facilisis nisi vel nibh luctus sit amet semper
           tellus gravida.
    <BLANKLINE>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus
      gravida.
    <BLANKLINE>
    Lorem is life
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus
      gravida.
    <BLANKLINE>
      Lorem always
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus
        gravida.
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
        Append content to this object.

        :param content: :class:`Paragraph` or :class:`Section` or :class:`DefinitionList` or ``None``.

        :return: self to allow chaining.
        """
        # @todo Accept one string. Make a paragraph with it.
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
        Format the document and return the generated string.
        """
        return "\n".join(self._formatContents(0))


class Section(Container):
    """
    A section in a document. Sections can be nested.
    """

    def __init__(self, title):
        Container.__init__(self)
        self.__title = title

    def _format(self, prefixLength):
        # @todo Add options to document, in particular one adding ":" after section titles and one adding ":" after terms in definition lists
        # @todo Add option to underline section titles
        # @todo Add option to leave blank line after section title
        return itertools.chain(_wrap(self.__title, prefixLength), self._formatContents(prefixLength + 2))


class Paragraph:
    """
    A paragraph in a document.
    """

    def __init__(self, text):
        # @todo Accept several strings
        self.__text = text

    def _format(self, prefixLength):
        return _wrap(self.__text, prefixLength)


class DefinitionList:
    """
    A list of terms with their definitions.

    >>> print Document().add(Section("Section title")
    ...   .add(DefinitionList()
    ...     .add("Item", Paragraph("Definition 1"))
    ...     .add("Other item", Paragraph("Definition 2"))
    ...   )
    ... ).format()
    Section title
      Item        Definition 1
      Other item  Definition 2
    """

    __maxDefinitionPrefixLength = 24

    def __init__(self):
        self.__items = []

    def add(self, name, definition):
        """
        Append a new term to the list.

        :param name: string.
        :param definition: :class:`Paragraph` or :class:`Section` or :class:`DefinitionList` or ``None``.

        :return: self to allow chaining.
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
