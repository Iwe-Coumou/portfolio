
class HTMLNode:
    tag: str
    value: str
    children: list
    props: dict
    
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError(f"This is not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return "None"
        return " ".join([""]+[f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, num_of_children: {len(self.children) if self.children else 0}, props: {self.props_to_html()})"