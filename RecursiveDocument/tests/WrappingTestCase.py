# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

from RecursiveDocument import Document, Section, Paragraph


class WrappingTestCase(unittest.TestCase):
    __lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus gravida. Proin lorem libero, aliquet vitae suscipit ac, egestas sit amet velit. In justo nisi, porttitor vel fermentum id, feugiat eget eros. Nullam vulputate risus tempor odio suscipit sit amet ornare est rhoncus. Vestibulum malesuada mattis sollicitudin. Duis ac lectus ac neque semper euismod imperdiet nec eros. Ut ac odio libero. Morbi a diam quis libero volutpat euismod. Etiam gravida fringilla erat quis facilisis. Morbi venenatis malesuada dapibus. Phasellus libero dui, congue a tincidunt ut, cursus in risus. Ut sapien sapien, scelerisque at hendrerit sed, vestibulum a sem. Sed vitae odio vel est aliquam suscipit ut gravida quam. Morbi a faucibus ipsum. In eros orci, feugiat et scelerisque non, faucibus et eros."
    __shortLorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque facilisis nisi vel nibh"

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        self.doc = Document()

    def testSingleParagraph(self):
        self.doc.add(Paragraph(self.__lorem))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
                facilisis nisi vel nibh luctus sit amet semper tellus gravida. Proin
                lorem libero, aliquet vitae suscipit ac, egestas sit amet velit. In
                justo nisi, porttitor vel fermentum id, feugiat eget eros. Nullam
                vulputate risus tempor odio suscipit sit amet ornare est rhoncus.
                Vestibulum malesuada mattis sollicitudin. Duis ac lectus ac neque
                semper euismod imperdiet nec eros. Ut ac odio libero. Morbi a diam
                quis libero volutpat euismod. Etiam gravida fringilla erat quis
                facilisis. Morbi venenatis malesuada dapibus. Phasellus libero dui,
                congue a tincidunt ut, cursus in risus. Ut sapien sapien, scelerisque
                at hendrerit sed, vestibulum a sem. Sed vitae odio vel est aliquam
                suscipit ut gravida quam. Morbi a faucibus ipsum. In eros orci,
                feugiat et scelerisque non, faucibus et eros.
                """
            )
        )

    def testParagraphInSubSection(self):
        self.doc.add(Section("Section").add(Section("Sub-section").add(Paragraph(self.__lorem))))
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Section:
                  Sub-section:
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Pellentesque facilisis nisi vel nibh luctus sit amet semper tellus
                    gravida. Proin lorem libero, aliquet vitae suscipit ac, egestas
                    sit amet velit. In justo nisi, porttitor vel fermentum id, feugiat
                    eget eros. Nullam vulputate risus tempor odio suscipit sit amet
                    ornare est rhoncus. Vestibulum malesuada mattis sollicitudin. Duis
                    ac lectus ac neque semper euismod imperdiet nec eros. Ut ac odio
                    libero. Morbi a diam quis libero volutpat euismod. Etiam gravida
                    fringilla erat quis facilisis. Morbi venenatis malesuada dapibus.
                    Phasellus libero dui, congue a tincidunt ut, cursus in risus. Ut
                    sapien sapien, scelerisque at hendrerit sed, vestibulum a sem. Sed
                    vitae odio vel est aliquam suscipit ut gravida quam. Morbi a
                    faucibus ipsum. In eros orci, feugiat et scelerisque non, faucibus
                    et eros.
                """
            )
        )

    def testLongSectionTitles(self):
        self.doc.add(
            Section("Section " + self.__shortLorem)
            .add(
                Section("Sub-section " + self.__shortLorem)
                .add(Paragraph("Some text"))
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Section Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Pellentesque facilisis nisi vel nibh:
                  Sub-section Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Pellentesque facilisis nisi vel nibh:
                    Some text
                """
            )
        )
