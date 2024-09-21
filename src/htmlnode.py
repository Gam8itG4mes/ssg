

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        
        html = ""
        for k in self.props.keys():
            html += f' {k}="{self.props[k]}"'

        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        if not self.tag:
            return (str(self.value))
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
        def __init__(self, tag, children, props=None):
            super().__init__(tag, None, children, props)

        
        def to_html(self):
            if not self.tag:
                raise ValueError("Object must have tag")
            
            if not self.children:
                raise ValueError("'Object must have children' - JD Vance")
            
            html = ""
            for c in self.children:
                html += c.to_html()
            

            return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"
        
        def __repr__(self):
            return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
