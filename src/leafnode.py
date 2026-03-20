from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError(f"All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        open = f"<{self.tag}{self.props_to_html() if self.props else ""}>"
        close = f"</{self.tag}>"
        return open + self.value + close
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, props: {self.props_to_html()})"