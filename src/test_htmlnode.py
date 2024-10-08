import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node1 = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node1.to_html()

    def test_repr(self):
        node1 = HTMLNode("p", "this is a test", None, {"href": "https://www.google.com","target": "_blank"})
        truth = "HTMLNode(p, this is a test, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(truth, repr(node1))

    def test_props_to_html(self):
        node1 = HTMLNode("p", "this is a test", None, {"href": "https://www.google.com","target": "_blank"})
        truth = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(truth, node1.props_to_html())

    def test_to_html_leaf_no_value(self):
        node1 = LeafNode(tag="a", value=None, props={"href": "https://www.google.com","target": "_blank"})
        with self.assertRaises(ValueError):
            node1.to_html()

    def test_to_html_leaf_no_tag(self):
        node1 = LeafNode(tag=None, value="this is a test", props=None)
        truth = "this is a test"
        self.assertTrue(truth, node1.to_html())

    def test_to_html_leaf_w_props(self):
        node1 = LeafNode("a", "this is a test", {"href": "https://www.google.com"})
        truth = '<a href="https://www.google.com">this is a test</a>'
        self.assertEqual(truth, node1.to_html())

    def test_to_html_leaf_wo_props(self):
        node1 = LeafNode(tag="a", value="this is a test", props=None)
        truth = "<a>this is a test</a>"
        self.assertEqual(truth, node1.to_html())

    def test_repr_leaf(self):
        node1 = LeafNode("a", "this is a test", {"href": "https://www.google.com"})
        truth = "LeafNode(a, this is a test, {'href': 'https://www.google.com'})"
        self.assertEqual(truth, repr(node1))

    def test_to_html_parent(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        truth = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertTrue(truth, node.to_html()) 

    def test_to_html_parent_no_tag(self):
        node = ParentNode(
        None,
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )   

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_parent_no_children(self):
        node = ParentNode(
        "a",
        None,
        )   

        with self.assertRaises(ValueError):
            node.to_html()
         
