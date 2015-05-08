# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import textwrap

from .. import Document, Section, DefinitionList, Paragraph, Container


class DefinitionListTestCase(unittest.TestCase):
    __shortLorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque facilisis nisi vel nibh"

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        self.doc = Document()

    def test_definition_list(self):
        self.doc.add(
            DefinitionList()
            .add("Item 1", Paragraph("Definition 1"))
            .add("Item 2", Paragraph("Definition 2"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Item 1  Definition 1
                Item 2  Definition 2"""
            )
        )

    def test_items_with_different_lengths(self):
        self.doc.add(
            DefinitionList()
            .add("Item 1", Paragraph("Definition 1"))
            .add("Longer item 2", Paragraph("Definition 2"))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Item 1         Definition 1
                Longer item 2  Definition 2"""
            )
        )

    def test_within_sub_section(self):
        self.doc.add(
            Section("Section")
            .add(
                Section("Sub-section")
                .add(
                    DefinitionList()
                    .add("Item 1", Paragraph("Definition 1"))
                    .add("Longer item 2", Paragraph("Definition 2"))
                )
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section
                  Sub-section
                    Item 1         Definition 1
                    Longer item 2  Definition 2"""
            )
        )

    def test_empty_definition(self):
        self.doc.add(
            DefinitionList()
            .add("Longer item 1", Paragraph("Definition 1"))
            .add("Item 2", Paragraph(""))
            .add("Longer item 3", Paragraph(""))
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Longer item 1  Definition 1
                Item 2
                Longer item 3"""
            )
        )

    def test_wrapping_of_definition_with_only_short_items(self):
        self.doc.add(
            Section("Section")
            .add(
                DefinitionList()
                .add("Item 1 (short enought)", Paragraph("Definition 1 " + self.__shortLorem))
                .add("Item 2", Paragraph("Definition 2 " + self.__shortLorem))
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Section
                  Item 1 (short enought)  Definition 1 Lorem ipsum dolor sit amet,
                                          consectetur adipiscing elit. Pellentesque
                                          facilisis nisi vel nibh
                  Item 2                  Definition 2 Lorem ipsum dolor sit amet,
                                          consectetur adipiscing elit. Pellentesque
                                          facilisis nisi vel nibh"""
            )
        )

    def test_wrapping_of_definition_with_short_and_long_items(self):
        self.doc.add(
            Section("Section")
            .add(
                DefinitionList()
                .add("Item 1 (just tooo long)", Paragraph("Definition 1 " + self.__shortLorem))
                .add("Item 2", Paragraph("Definition 2 " + self.__shortLorem))
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Section
                  Item 1 (just tooo long)
                          Definition 1 Lorem ipsum dolor sit amet, consectetur
                          adipiscing elit. Pellentesque facilisis nisi vel nibh
                  Item 2  Definition 2 Lorem ipsum dolor sit amet, consectetur
                          adipiscing elit. Pellentesque facilisis nisi vel nibh"""
            )
        )

    def test_wrapping_of_definition_with_only_long_items(self):
        self.doc.add(
            Section("Section")
            .add(
                DefinitionList()
                .add("Item 1 (just tooo long)", Paragraph("Definition 1 " + self.__shortLorem))
                .add("Item 2 (also too long, really)", Paragraph("Definition 2 " + self.__shortLorem))
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent(
                # 70 chars ###########################################################
                """\
                Section
                  Item 1 (just tooo long)
                    Definition 1 Lorem ipsum dolor sit amet, consectetur adipiscing
                    elit. Pellentesque facilisis nisi vel nibh
                  Item 2 (also too long, really)
                    Definition 2 Lorem ipsum dolor sit amet, consectetur adipiscing
                    elit. Pellentesque facilisis nisi vel nibh"""
            )
        )

    def test_container_as_definition(self):
        self.doc.add(
            Section("Section")
            .add(
                DefinitionList()
                .add("Item", Container().add(Paragraph("Para 1")).add(Paragraph("Para 2")))
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section
                  Item  Para 1

                        Para 2"""
            )
        )

    def test_definition_list_as_definition(self):
        self.doc.add(
            Section("Section")
            .add(
                DefinitionList()
                .add(
                    "Item 1",
                    DefinitionList()
                    .add("Item A", Paragraph("Definition A"))
                    .add("Item B", Paragraph("Definition B"))
                )
                .add(
                    "Item 2",
                    DefinitionList()
                    .add("Item C", Paragraph("Definition C"))
                    .add("Item D", Paragraph("Definition D"))
                )
            )
        )
        self.assertEqual(
            self.doc.format(),
            textwrap.dedent("""\
                Section
                  Item 1  Item A  Definition A
                          Item B  Definition B
                  Item 2  Item C  Definition C
                          Item D  Definition D"""
            )
        )
