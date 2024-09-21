from htmlnode import LeafNode

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
    
def text_node_to_html_node(text_node: TextNode):

    
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