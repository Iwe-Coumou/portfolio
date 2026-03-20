from funcs import extract_markdown_images, extract_markdown_links
import unittest


class TestRegexExtract(unittest.TestCase):

    # --- extract_markdown_images ---
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![cat](https://example.com/cat.png) and ![dog](https://example.com/dog.png)"
        )
        self.assertListEqual([
            ("cat", "https://example.com/cat.png"),
            ("dog", "https://example.com/dog.png"),
        ], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_none_present(self):
        matches = extract_markdown_images("This is just plain text with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_does_not_match_links(self):
        # a plain link should not be captured as an image
        matches = extract_markdown_images(
            "This is a [link](https://example.com) not an image."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_mixed_with_links(self):
        # only images should be returned, not links
        matches = extract_markdown_images(
            "![img](https://example.com/img.png) and [link](https://example.com)"
        )
        self.assertListEqual([("img", "https://example.com/img.png")], matches)

    # --- extract_markdown_links ---
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Visit [Google](https://google.com) and [GitHub](https://github.com)"
        )
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ], matches)

    def test_extract_markdown_links_none_present(self):
        matches = extract_markdown_links("Just plain text here.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_does_not_match_images(self):
        # images should not be captured as links
        matches = extract_markdown_links(
            "![image](https://example.com/img.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed_with_images(self):
        # only links should be returned, not images
        matches = extract_markdown_links(
            "![img](https://example.com/img.png) and [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_empty_anchor_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)


if __name__ == "__main__":
    unittest.main()