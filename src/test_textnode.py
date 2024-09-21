import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node1 = TextNode("This is a text node", "bold", "bom.com")
        node2 = TextNode("This is a text node", "bold", "bom.com")
        self.assertEqual(node1, node2)  

    def test_not_eq(self):
        node1 = TextNode("This is a text node", "italic", "bom.com")
        node2 = TextNode("This is a text node", "bold", "bom.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", "italic", "bom.com")
        truth = 'TextNode(This is a text node, italic, bom.com)'
        self.assertEqual(truth, repr(node1))


if __name__ == "__main__":
    unittest.main()
        
