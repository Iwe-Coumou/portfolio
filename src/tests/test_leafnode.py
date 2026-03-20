import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_props_none(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.props, None)
        
    def test_childrend(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.children, None)
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold!")
        self.assertEqual(node.to_html(), "<b>This is bold!</b>")
        
    def test_leaf_to_html_li(self):
        node = LeafNode("li", "This is a list item")
        self.assertEqual(node.to_html(), "<li>This is a list item</li>")