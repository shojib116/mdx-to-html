import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "p",
            "hello",
            ["child1", "child2"],
            {"class": "text-bold"},
        )
        expected = "HTMLNode(p, hello, ['child1', 'child2'], {'class': 'text-bold'})"
        self.assertEqual(repr(node), expected)   
        
    def test_props_to_html_with_props(self):
        node = HTMLNode(
            "a",
            "link",
            None,
            {"href": "https://example.com", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(),
            "href='https://example.com' target='_blank'",
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello", None, None)
        self.assertEqual(node.props_to_html(), "")
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")   

    def test_leaf_to_html_a(self):   
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Click me!</a>")


if __name__ == "__main__":
    unittest.main()
