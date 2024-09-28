from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
text_type_fail = "fail"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else: 
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text, None)
        case "bold":
            return LeafNode("b", text_node.text, None)
        case "italic":
            return LeafNode("i", text_node.text, None)
        case "code":
            return LeafNode("code", text_node.text,None)
        case "link":
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case "image":
            return LeafNode("img", None, {"src": text_node.url, "alt":text_node.text})
        case _:
            raise ValueError(f"Text type {text_node.text_type} not valid.")
        
def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        split_list = []
        splits = old_node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError(f"Delimiter '{delimiter}' not closed")
        for i in range(len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                split_list.append(TextNode(splits[i], text_type_text))
            else:
                split_list.append(TextNode(splits[i], text_type))
        new_nodes.extend(split_list)
    return new_nodes

def extract_markdown_images(text):
    matches  = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches  = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list)-> list:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            # print("no images")
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                # I honestly dont know if this ever gets reached? 
                # I literally cannot get this to fail
                # because if I put in bad markdown in the test,
                # extract_markdown will just return 0 images
                # and we continue on our merry way
                raise ValueError("Invalid Markdown for image")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))

            new_nodes.append(TextNode(image[0], text_type_image, image[1]))

            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
    
        text  = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid Markdown for link")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

    
def text_to_text_nodes(text):
    foo = TextNode(text, text_type_text)

    bold = split_nodes_delimiter([foo], "**", text_type_bold)
    italics = split_nodes_delimiter(bold, "*", text_type_italic)
    code = split_nodes_delimiter(italics, "`", text_type_code)
    images = split_nodes_image(code)
    links = split_nodes_link(images)

    return links