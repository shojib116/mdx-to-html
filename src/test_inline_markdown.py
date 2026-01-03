import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter  

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter_simple(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode(
            "Hello _world_!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_are_untouched(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_invalid_markdown_raises(self):
        node = TextNode(
            "This is **broken",
            TextType.TEXT,
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == '__main__':
    unittest.main()
