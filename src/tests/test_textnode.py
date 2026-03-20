import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, bold, None)")
        
    def test_ineq(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        node2 = TextNode("This is a link", TextType.LINK, "https://localhost:8888")
        self.assertNotEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("This is not a link or image", TextType.TEXT)
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()