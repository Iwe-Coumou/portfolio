import unittest
from textnode import TextNode, TextType
from funcs import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):

    # --- split_nodes_image ---
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_single(self):
        node = TextNode(
            "Text before ![cat](https://example.com/cat.png) text after",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![cat](https://example.com/cat.png) text after",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Text before ![cat](https://example.com/cat.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        self.assertListEqual(
            [TextNode("Just plain text.", TextType.TEXT)],
            split_nodes_image([node]),
        )

    def test_split_images_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertListEqual(
            [TextNode("already bold", TextType.BOLD)],
            split_nodes_image([node]),
        )

    # --- split_nodes_link ---
    def test_split_links_multiple(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [GitHub](https://github.com) today",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(" today", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_single(self):
        node = TextNode(
            "Click [here](https://example.com) to continue",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" to continue", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_at_start(self):
        node = TextNode("[home](https://example.com) some text after", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("home", TextType.LINK, "https://example.com"),
                TextNode(" some text after", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_at_end(self):
        node = TextNode("some text before [home](https://example.com)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("some text before ", TextType.TEXT),
                TextNode("home", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        self.assertListEqual(
            [TextNode("Just plain text.", TextType.TEXT)],
            split_nodes_link([node]),
        )

    def test_split_links_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertListEqual(
            [TextNode("already bold", TextType.BOLD)],
            split_nodes_link([node]),
        )

    def test_split_links_does_not_capture_images(self):
        node = TextNode(
            "![img](https://example.com/img.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        for n in result:
            self.assertNotEqual(n.text_type, TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()