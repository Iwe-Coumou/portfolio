import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode(tag="blockquote", value="This is a quote.")
        self.assertEqual(node.__repr__(), "HTMLNode(blockquote, This is a quote., num_of_children: 0, props: None)")
    
    def test_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        
    def test_propt_to_html(self):
        node = HTMLNode(tag='img', props={"src": "url/of/image.jpg", "alt": "Description of image"})
        self.assertEqual(node.props_to_html(), ' src="url/of/image.jpg" alt="Description of image"')

if __name__ == "__main__":
    unittest.main()