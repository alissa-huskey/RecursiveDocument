# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

from .. import Document, Section, Paragraph, Container


class IndentationTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.doc = Document()

    def test_empty_document(self):
        self.assertEqual(self.doc.format(), "")

    def test_add_none_is_no_op(self):
        self.doc.add(None)
        self.assertEqual(self.doc.format(), "")

    def test_one_section_with_one_paragraph(self):
        self.doc.add(
            Section("First section")
            .add(Paragraph("Some text"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                First section
                  Some text"""
            )
        )

    def test_one_section_with_two_paragraphs(self):
        self.doc.add(
            Section("First section")
            .add(Paragraph("Some text"))
            .add(Paragraph("Some other text"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                First section
                  Some text

                  Some other text"""
            )
        )

    def test_several_sections_with_several_paragraphs(self):
        self.doc.add(
            Section("Section A")
            .add(Paragraph("Text A.1"))
            .add(Paragraph("Text A.2"))
            .add(Paragraph("Text A.3"))
        ).add(
            Section("Section B")
            .add(Paragraph("Text B.1"))
            .add(Paragraph("Text B.2"))
            .add(Paragraph("Text B.3"))
        ).add(
            Section("Section C")
            .add(Paragraph("Text C.1"))
            .add(Paragraph("Text C.2"))
            .add(Paragraph("Text C.3"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section A
                  Text A.1

                  Text A.2

                  Text A.3

                Section B
                  Text B.1

                  Text B.2

                  Text B.3

                Section C
                  Text C.1

                  Text C.2

                  Text C.3"""
            )
        )

    def test_paragraph_then_section(self):
        self.doc.add(
            Paragraph("Some text")
        ).add(
            Section("Section title")
            .add(Paragraph("Section text"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Some text

                Section title
                  Section text"""
            )
        )

    def test_section_then_paragraph(self):
        self.doc.add(
            Section("Section title")
            .add(Paragraph("Section text"))
        ).add(
            Paragraph("Some text")
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section title
                  Section text

                Some text"""
            )
        )

    def test_empty_section(self):
        self.doc.add(
            Section("Empty section title")
        ).add(
            Paragraph("Some text")
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Empty section title

                Some text"""
            )
        )

    def test_imbricated_sections(self):
        self.doc.add(
            Section("Section A")
            .add(Section("Section A.1").add(Paragraph("Text A.1.a")).add(Paragraph("Text A.1.b")))
            .add(Section("Section A.2").add(Paragraph("Text A.2.a")).add(Paragraph("Text A.2.b")))
        ).add(
            Section("Section B")
            .add(Section("Section B.1").add(Paragraph("Text B.1.a")).add(Paragraph("Text B.1.b")))
            .add(Section("Section B.2").add(Paragraph("Text B.2.a")).add(Paragraph("Text B.2.b")))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section A
                  Section A.1
                    Text A.1.a

                    Text A.1.b

                  Section A.2
                    Text A.2.a

                    Text A.2.b

                Section B
                  Section B.1
                    Text B.1.a

                    Text B.1.b

                  Section B.2
                    Text B.2.a

                    Text B.2.b"""
            )
        )

    def test_recursive_containers_issame_as_flat_container(self):
        self.doc.add(
            Container()
            .add(Paragraph("P1"))
            .add(Paragraph("P2"))
            .add(
                Container()
                .add(Paragraph("P3"))
                .add(Paragraph("P4"))
                .add(
                    Container()
                    .add(Paragraph("P5"))
                )
                .add(
                    Container()
                    .add(Paragraph("P6"))
                )
            )
            .add(Paragraph("P7"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                P1

                P2

                P3

                P4

                P5

                P6

                P7"""
            )
        )

    def test_empty_container(self):
        self.doc.add(Container())
        self.assertEqual(self.doc.format(), "")

    def test_empty_section_2(self):
        self.doc.add(Section("Title"))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Title"""
            )
        )

    def test_recursive_empty_containers(self):
        self.doc.add(
            Container().add(
                Container().add(
                    Container().add(
                        Container()
                    )
                )
            )
        )
        self.assertEqual(self.doc.format(), "")

    def test_successive_empty_containers(self):
        self.doc.add(
            Container()
        ).add(
            Container()
        ).add(
            Container()
        ).add(
            Container()
        ).add(
            Container()
        )
        self.assertEqual(self.doc.format(), "")

    def test_empty_containers_after_paragraph(self):
        self.doc.add(
            Paragraph("Foobar")
        ).add(
            Container()
        ).add(
            Container()
        )
        self.assertEqual(self.doc.format(), "Foobar")

    def test_empty_containers_before_paragraph(self):
        self.doc.add(
            Container()
        ).add(
            Container()
        ).add(
            Paragraph("Foobar")
        )
        self.assertEqual(self.doc.format(), "Foobar")
