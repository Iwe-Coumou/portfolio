import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
        # --- error cases ---
    def test_raises_without_tag(self):
        child = LeafNode("span", "hi")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_raises_with_empty_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_raises_with_none_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # --- props ---
    def test_to_html_with_props(self):
        child = LeafNode("span", "text")
        node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>text</span></div>')

    def test_to_html_with_multiple_props(self):
        child = LeafNode("span", "text")
        node = ParentNode("a", [child], {"href": "https://example.com", "target": "_blank"})
        html = node.to_html()
        # check structure without assuming prop order
        self.assertTrue(html.startswith("<a "))
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.endswith("<span>text</span></a>"))

    # --- multiple children ---
    def test_multiple_leaf_children(self):
        node = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(node.to_html(), "<p><b>bold</b> and <i>italic</i></p>")

    def test_mixed_parent_and_leaf_children(self):
        node = ParentNode("div", [
            LeafNode("p", "first"),
            ParentNode("ul", [
                LeafNode("li", "item"),
            ]),
        ])
        self.assertEqual(node.to_html(), "<div><p>first</p><ul><li>item</li></ul></div>")

    # --- deep nesting ---
    def test_deeply_nested_parents(self):
        # div > section > article > p > b
        inner = LeafNode("b", "deep")
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("article", [
                    ParentNode("p", [inner])
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p><b>deep</b></p></article></section></div>",
        )

    def test_multiple_children_at_each_level(self):
        node = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "one"),
                LeafNode("li", "two"),
                LeafNode("li", "three"),
            ]),
            ParentNode("ul", [
                LeafNode("li", "four"),
                LeafNode("li", "five"),
            ]),
        ])
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<ul><li>one</li><li>two</li><li>three</li></ul>"
            "<ul><li>four</li><li>five</li></ul>"
            "</div>",
        )