import unittest
from funcs import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extracts_title(self):
        markdown = "# Hello World\n\nSome paragraph"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_raises_if_no_h1(self):
        markdown = "## Not a title\n\nSome paragraph"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_ignores_h2_and_below(self):
        markdown = "### Section\n\nSome paragraph"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_strips_whitespace(self):
        markdown = "#   Spaced Title\n\nSome paragraph"
        self.assertEqual(extract_title(markdown), "Spaced Title")