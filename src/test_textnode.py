import unittest
from textnode import (
    TextNode, 
    text_node_to_html_node,
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link, text_to_text_nodes
)

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


class TestInlineMarkdown(unittest.TestCase):
    def test_split_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_split_delim_italic(self):
        node = TextNode(
            "This is text with an *italic* word", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text)
            ],
            new_nodes
        )

    def test_split_delim_code(self):
        node = TextNode(
            "This text has a `code block` in it", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This text has a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" in it", text_type_text)
            ],
            new_nodes
        )

    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        truth = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(
            truth,
            extract_markdown_images(text)
        )

    def test_extract_image2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        truth = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertListEqual(
            truth,
            extract_markdown_images(text)
        )

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        truth = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(
            truth,
            extract_markdown_links(text)
        )

    def test_extract_link2(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        truth = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(
            truth,
            extract_markdown_links(text)
        )

    def test_split_node_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
             text_type_text,
            )
        truth = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(truth,
        split_nodes_link([node]) )

    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
             text_type_text,
            )
        truth = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
        ]
        self.assertListEqual(truth,
        split_nodes_link([node]) )

    def test_split_node_images(self):
        node = TextNode(
            "This is text with images ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
             text_type_text,
            )
        truth = [
            TextNode("This is text with images ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(truth,
        split_nodes_image([node]) )

    def test_split_node_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev)",
             text_type_text,
            )
        truth = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
        ]
        self.assertListEqual(truth,
        split_nodes_image([node]) )

    def test_text_to_textnodes(self):
        string = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        truth = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(truth, text_to_text_nodes(string)) 

if __name__ == "__main__":
    unittest.main()
        
