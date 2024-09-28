import unittest
from htmlnode import HTMLNode
from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_olist,
    block_type_ulist
)


class TestBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        truth = ['# This is a heading', 
                 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                 '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                ]
        self.assertListEqual(truth,
        markdown_to_blocks(markdown=markdown))

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    
    def test_block_to_block_type_headings(self):
        md = "# This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))
        md = "## This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))
        md = "### This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))
        md = "#### This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))
        md = "##### This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))
        md = "###### This is a heading"
        self.assertEqual(block_type_heading, block_to_block_type(md))

    def test_block_to_block_type_code(self):
        md ="```\nprint('Hello, world')\n```"
        self.assertEqual(block_type_code, block_to_block_type(md))

    def test_block_to_block_type_quote(self):
        md = """> Quoth the Raven, 'Nevermore'\n> All the worlds a stage"""
        self.assertEqual(block_type_quote, block_to_block_type(md))

    def test_block_to_block_type_ul_dash(self):
        md = "- list\n- listy"
        self.assertEqual(block_type_ulist, block_to_block_type(md))

    def test_block_to_block_type_ul_star(self):
        md = "* list\n* listy"
        self.assertEqual(block_type_ulist, block_to_block_type(md))
    
    def test_block_to_block_type_ol(self):
        md = "1. In\n2. Order"
        self.assertEqual(block_type_olist, block_to_block_type(md))

    def test_block_to_block_type_paragraph(self):
        md = "Just some stuff"
        self.assertEqual(block_type_paragraph, block_to_block_type(md))

    def test_md_to_html_node(self):
        md = "######## Just some stuff"
        truth = HTMLNode(tag="div", value=None, children=
                        [HTMLNode("p", "Just some stuff", None, None)]
        , props=None)
        test  = markdown_to_html_node(md)
        self.assertEqual(truth.tag, test.tag)
        self.assertEqual(truth.value, test.value)
        self.assertIsNotNone(truth.children, test.children)
        self.assertIsInstance(test.children, list)
        self.assertEqual(truth.props, test.props)

if __name__ == "__main__":
    unittest.main()
