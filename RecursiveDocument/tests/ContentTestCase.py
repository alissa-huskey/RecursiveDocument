# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

from .. import Document, Section, DefinitionList, Paragraph, Container

class ContentTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.doc = Document()

    def test_add_string_to_doc(self):
        self.doc.add("This is a plain string")
        self.assertEqual(self.doc.format(), "This is a plain string")

    def test_add_several_things_to_doc(self):
        self.doc.add("Plain string", None, Section("Foo").add("Bar baz."))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Plain string

                Foo
                  Bar baz."""
            )
        )

    def test_string_as_definition(self):
        self.doc.add(DefinitionList().add("term", "plain string"))
        self.assertEqual(self.doc.format(), "term  plain string")

    def test_none_as_definition(self):
        self.doc.add(DefinitionList().add("term 1", "def 1").add("term 2", None).add("term 3", "def 3"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                term 1  def 1
                term 2
                term 3  def 3"""
            )
        )
