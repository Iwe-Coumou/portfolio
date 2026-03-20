import unittest
from textnode import TextNode, TextType
from funcs import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):

    def test_all_types(self):
        text = "This is **bold** and _italic_ and `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            text_to_textnodes("just plain text"),
        )

    def test_bold_only(self):
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("this is **bold** text"),
        )

    def test_italic_only(self):
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("this is _italic_ text"),
        )

    def test_code_only(self):
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("this is `code` text"),
        )

    def test_image_only(self):
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("this is ![img](https://example.com/img.png) text"),
        )

    def test_link_only(self):
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes("this is [link](https://example.com) text"),
        )

    def test_multiple_bold(self):
        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            text_to_textnodes("**one** and **two**"),
        )

    def test_adjacent_types(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("**bold**_italic_"),
        )


if __name__ == "__main__":
    unittest.main()