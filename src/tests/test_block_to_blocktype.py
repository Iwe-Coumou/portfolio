import unittest
from blocks import BlockType
from funcs import block_to_blocktype


class TestBlockToBlockType(unittest.TestCase):

    # --- heading ---
    def test_heading_h1(self):
        self.assertEqual(block_to_blocktype("# Heading 1"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_blocktype("### Heading 3"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_blocktype("###### Heading 6"), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_blocktype("####### too many"), BlockType.PARAGRAPH)

    # --- code ---
    def test_code_block(self):
        self.assertEqual(block_to_blocktype("```\nsome code\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_blocktype("```\nline one\nline two\n```"), BlockType.CODE)

    def test_code_block_no_newline_after_backticks_is_paragraph(self):
        self.assertEqual(block_to_blocktype("```some code```"), BlockType.PARAGRAPH)

    # --- quote ---
    def test_quote_single_line(self):
        self.assertEqual(block_to_blocktype(">this is a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_blocktype(">line one\n>line two\n>line three"), BlockType.QUOTE)

    def test_quote_one_line_missing_marker_is_paragraph(self):
        self.assertEqual(block_to_blocktype(">line one\nline two"), BlockType.PARAGRAPH)

    # --- unordered list ---
    def test_unordered_list_single(self):
        self.assertEqual(block_to_blocktype(" - item one"), BlockType.U_List)

    def test_unordered_list_multiple(self):
        self.assertEqual(block_to_blocktype(" - item one\n - item two\n - item three"), BlockType.U_List)

    def test_unordered_list_missing_marker_is_paragraph(self):
        self.assertEqual(block_to_blocktype(" - item one\nitem two"), BlockType.PARAGRAPH)

    # --- ordered list ---
    def test_ordered_list_single(self):
        self.assertEqual(block_to_blocktype("1. item one"), BlockType.O_LIST)

    def test_ordered_list_multiple(self):
        self.assertEqual(block_to_blocktype("1. item one\n2. item two\n3. item three"), BlockType.O_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        self.assertEqual(block_to_blocktype("2. item one\n3. item two"), BlockType.PARAGRAPH)

    def test_ordered_list_non_incrementing_is_paragraph(self):
        self.assertEqual(block_to_blocktype("1. item one\n3. item two"), BlockType.PARAGRAPH)

    # --- paragraph ---
    def test_paragraph(self):
        self.assertEqual(block_to_blocktype("just a plain paragraph"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_blocktype("line one\nline two"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()