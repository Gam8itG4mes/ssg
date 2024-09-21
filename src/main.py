from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("Node", "bold", "https://www.get-rekd.com")
    print(text_node)



if __name__ == "__main__":
    main()
