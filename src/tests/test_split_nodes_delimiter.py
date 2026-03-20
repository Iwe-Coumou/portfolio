import unittest
from textnode import TextNode, TextType
from funcs import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    # --- basic single delimiter ---
    def test_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold_single(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_italic_single(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    # --- multiple delimiters in one node ---
    def test_multiple_bold(self):
        node = TextNode("**one** and **two** are bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" are bold", TextType.TEXT),
        ])

    def test_multiple_code_spans(self):
        node = TextNode("call `foo()` then `bar()`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("call ", TextType.TEXT),
            TextNode("foo()", TextType.CODE),
            TextNode(" then ", TextType.TEXT),
            TextNode("bar()", TextType.CODE),
        ])

    # --- delimiter at start or end ---
    def test_delimiter_at_start(self):
        node = TextNode("**bold** at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("ends with **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("ends with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    # --- non-TEXT nodes pass through untouched ---
    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_list_only_splits_text_nodes(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("plain with `code` inside", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("already bold", TextType.BOLD),
            TextNode("plain with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ])

    # --- no delimiter present ---
    def test_no_delimiter_returns_original(self):
        node = TextNode("plain text no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("plain text no delimiters", TextType.TEXT)])

    # --- unclosed delimiter raises ---
    def test_unclosed_delimiter_raises(self):
        node = TextNode("this is **unclosed", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()