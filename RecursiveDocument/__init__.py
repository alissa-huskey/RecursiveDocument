# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
RecursiveDocument does absolutely nothing fancy (Italic? Bold? Underline? No!).
It just prints your document on 70 columns and it does it well.
It was written for help messages in `InteractiveCommandLine <http://pythonhosted.org/InteractiveCommandLine/>`__
and released separately because, well, you know, reusability.

Introduction
------------

Import:

    >>> from RecursiveDocument import Document, Section
    >>> from RecursiveDocument import Paragraph, DefinitionList

Create a simple document and format it:

    >>> doc = Document()
    >>> doc.add("Some text")
    <RecursiveDocument.Document ...>
    >>> doc.add("Some other text")
    <RecursiveDocument.Document ...>
    >>> print doc.format()
    Some text
    <BLANKLINE>
    Some other text

Add
---

Because ``add`` returns ``self``, RecursiveDocument allows chaining of calls to ``add``:

    >>> print Document().add("Some text").add("Some other text").format()
    Some text
    <BLANKLINE>
    Some other text

``add`` is also variadic so you can add several things at once:

    >>> print Document().add("Some text", "Some other text").format()
    Some text
    <BLANKLINE>
    Some other text

Wrapping
--------

When the document is wide, it is wrapped to 70 caracters:

    >>> lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus gravida."

    >>> print Document().add(
    ...   lorem + " " + lorem,
    ...   lorem + " " + lorem,
    ... ).format()
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida. Lorem
    ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida.
    <BLANKLINE>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida. Lorem
    ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
    facilisis nisi vel nibh luctus sit amet semper tellus gravida.

Sections
--------

Sections and sub-sections can be nested.
They are indented by 2 spaces to improve readability:

    >>> print Document().add(
    ...   Section("First section").add(
    ...     "Some text.",
    ...     Section("Sub-section").add("This is so deep."),
    ...     "This is not that deep.",
    ...   ),
    ...   Section("Second section").add(
    ...     "Some other text.",
    ...   ),
    ... ).format()
    First section
      Some text.
    <BLANKLINE>
      Sub-section
        This is so deep.
    <BLANKLINE>
      This is not that deep.
    <BLANKLINE>
    Second section
      Some other text.

Paragraphs
----------

When you add a string, it's like adding a :class:`Paragraph` containing this string:

    >>> print Document().add(
    ...   Paragraph("Some text"),
    ...   Paragraph("Some other text"),
    ... ).format()
    Some text
    <BLANKLINE>
    Some other text

You can also create a :class:`Paragraph` from several strings:

    >>> print Document().add(
    ...   Paragraph("Some text.", "Some other text.")
    ... ).format()
    Some text. Some other text.

Definition lists
----------------

    >>> print Document().add(
    ...   DefinitionList()
    ...     .add("term 1", "definition 1")
    ...     .add(
    ...       "term 2",
    ...       Section("definition 2 is a section")
    ...         .add("With some text. Can you believe it?")
    ...         .add("Oh, and next term has no definition.")
    ...     )
    ...     .add("term 3", None)
    ...     .add("longest term", "The longest term decides on which column definitions start.")
    ...     .add("very very very very long term", "Except that this term is so long that we couldn't put it's definition on the same line. So we didn't shrink other terms' definitions.")
    ... ).format()
    term 1        definition 1
    term 2        definition 2 is a section
                    With some text. Can you believe it?
    <BLANKLINE>
                    Oh, and next term has no definition.
    term 3
    longest term  The longest term decides on which column definitions
                  start.
    very very very very long term
                  Except that this term is so long that we couldn't put
                  it's definition on the same line. So we didn't shrink
                  other terms' definitions.
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

    # @todo Maybe use @variadic
    def add(self, *contents):
        """
        Append contents to this object.

        :param contents: one or several :class:`Paragraph` or string (a :class:`Paragraph` will be created for you) or :class:`Section` or :class:`DefinitionList` or ``None``.

        :return: self to allow chaining.
        """
        for content in contents:
            if isinstance(content, basestring):
                content = Paragraph(content)
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
        return itertools.chain(_wrap(self.__title, prefixLength), self._formatContents(prefixLength + 2))


class Paragraph:
    """
    A paragraph in a document.

    :param text: one or more strings.
    """

    def __init__(self, *text):
        self.__text = " ".join(text)

    def _format(self, prefixLength):
        return _wrap(self.__text, prefixLength)


class Empty:
    def _format(self, prefixLength):
        return ""


EMPTY = Empty()


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

    # @todo Find a way to make variadic as well
    def add(self, name, definition):
        """
        Append a new term to the list.

        :param name: string.
        :param definition: :class:`Paragraph` or string (a :class:`Paragraph` will be created for you) or :class:`Section` or :class:`DefinitionList` or ``None``.

        :return: self to allow chaining.
        """
        if isinstance(definition, basestring):
            definition = Paragraph(definition)
        if definition is None:
            definition = EMPTY
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
