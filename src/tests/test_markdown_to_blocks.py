import unittest
from funcs import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            markdown_to_blocks(md),
        )

    def test_single_block(self):
        md = "This is a single paragraph with no blank lines."
        self.assertEqual(
            ["This is a single paragraph with no blank lines."],
            markdown_to_blocks(md),
        )

    def test_strips_leading_trailing_whitespace(self):
        md = """
   some block with whitespace   

   another block   
"""
        self.assertEqual(
            ["some block with whitespace", "another block"],
            markdown_to_blocks(md),
        )

    def test_removes_empty_blocks(self):
        md = """
first block


second block



third block
"""
        self.assertEqual(
            ["first block", "second block", "third block"],
            markdown_to_blocks(md),
        )

    def test_heading_paragraph_list(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        self.assertEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
            markdown_to_blocks(md),
        )

    def test_empty_string(self):
        self.assertEqual([], markdown_to_blocks(""))

    def test_only_newlines(self):
        self.assertEqual([], markdown_to_blocks("\n\n\n\n"))

    def test_inline_newlines_preserved(self):
        # newlines within a block should not be treated as separators
        md = """
line one
line two
line three

new block
"""
        self.assertEqual(
            ["line one\nline two\nline three", "new block"],
            markdown_to_blocks(md),
        )


if __name__ == "__main__":
    unittest.main()