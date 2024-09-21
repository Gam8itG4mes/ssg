import unittest
from textnode import TextNode, text_node_to_html_node

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_type_fail
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node1 = TextNode("This is a text node", text_type_bold, "bom.com")
        node2 = TextNode("This is a text node", text_type_bold, "bom.com")
        self.assertEqual(node1, node2)  

    def test_not_eq(self):
        node1 = TextNode("This is a text node", text_type_italic, "bom.com")
        node2 = TextNode("This is a text node", text_type_bold, "bom.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", text_type_italic, "bom.com")
        truth = 'TextNode(This is a text node, italic, bom.com)'
        self.assertEqual(truth, repr(node1))


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text_node.text)

    def test_bold(self):
        text_node = TextNode("this is bold text", text_type_bold)
        html_node = text_node_to_html_node(text_node=text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, text_node.text)

    def test_italic(self):
        text_node = TextNode("this is italics", text_type_italic)
        html_node = text_node_to_html_node(text_node=text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, text_node.text)

    def test_code(self):
        text_node = TextNode("this is code", text_type_code)
        html_node = text_node_to_html_node(text_node=text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, text_node.text)

    def test_link(self):
        text_node = TextNode("this is a link", text_type_link, "google.com")
        html_node = text_node_to_html_node(text_node=text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.props, {'href':f'{text_node.url}'})

    def test_image(self):
        text_node = TextNode("This is alt text", text_type_image, "bomb.com/img.png")
        html_node = text_node_to_html_node(text_node=text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {'src':f'{text_node.url}', 'alt':f'{text_node.text}'})

    def test_invalid(self):
        text_node = TextNode("this should raise value error", text_type_fail)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()
        
