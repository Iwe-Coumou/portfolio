from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError(f"Parent nodes must have children")
        
        open = f"<{self.tag}{self.props_to_html() if self.props else ""}>"
        close = f"</{self.tag}>"
        body = "".join(node.to_html() for node in self.children)
        return open + body + close