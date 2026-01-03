import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_links, text_to_textnodes  

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_does_not_extract_links(self):
        matches = extract_markdown_images("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_does_not_extract_images(self):
        matches = extract_markdown_links("This is text with an ![link](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

class TestSplitNodeImage(unittest.TestCase):
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


    def test_split_images_no_images(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Just some plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_single_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_image_at_end(self):
        node = TextNode(
            "Some text then ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text then ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode(
                "First ![one](https://i.imgur.com/1.png)",
                TextType.TEXT,
            ),
            TextNode(
                "Then ![two](https://i.imgur.com/2.png) done",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode("Then ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://i.imgur.com/2.png"),
                TextNode(" done", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [],
            new_nodes,
        )
    
    def test_split_images_alt_with_spaces_and_punctuation(self):
        node = TextNode(
            "Look ![my great image!](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Look ", TextType.TEXT),
                TextNode(
                    "my great image!",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
            ],
            new_nodes,
        )

class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links_no_links(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode("Just some plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_single_link_only(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode(
                    "boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                )
            ],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev) and some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode(
                    "boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode(
            "Some text then [boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Some text then ", TextType.TEXT),
                TextNode(
                    "boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple_links_one_node(self):
        node = TextNode(
            "Go to [boot dev](https://www.boot.dev) and then [YouTube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode(
                    "boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and then ", TextType.TEXT),
                TextNode(
                    "YouTube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode(
                "First [one](https://example.com/1)",
                TextType.TEXT,
            ),
            TextNode(
                "Then [two](https://example.com/2) done",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://example.com/1"),
                TextNode("Then ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://example.com/2"),
                TextNode(" done", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_preserves_non_text_nodes(self):
        code_node = TextNode("some code", TextType.CODE)
        text_node = TextNode(
            "Link to [site](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([code_node, text_node])
        self.assertListEqual(
            [
                code_node,
                TextNode("Link to ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_alt_text_with_spaces_and_punctuation(self):
        node = TextNode(
            "Look at [my great link!](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Look at ", TextType.TEXT),
                TextNode("my great link!", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_only(self):
        text = "Just some plain text."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("Just some plain text.", TextType.TEXT)],
            nodes,
        )

    def test_bold_only(self):
        text = "This is **bold**."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_italic_only(self):
        text = "This is _italic_."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_code_only(self):
        text = "Inline `code` here."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Inline ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here.", TextType.TEXT),
            ],
            nodes,
        )

    def test_image_only(self):
        text = "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode(
                    "obi wan",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                )
            ],
            nodes,
        )

    def test_link_only(self):
        text = "[boot dev](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_full_mixed_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_mixed_without_images_or_links(self):
        text = "Start **bold** and _italic_ and `code` end."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" end.", TextType.TEXT),
            ],
            nodes,
        )



if __name__ == '__main__':
    unittest.main()
