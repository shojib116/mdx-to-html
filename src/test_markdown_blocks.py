import unittest
from markdown_blocks import (
    markdown_to_blocks, 
    block_to_block_type, 
    BlockType, 
    is_ordered_list_block, 
    markdown_to_html_node
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""

        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_empty_string(self):
        markdown = ""
        expected_blocks = []
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_single_block(self):
        markdown = "Just a single block of text."
        expected_blocks = ["Just a single block of text."]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

    def test_multiple_empty_lines(self):
        markdown = "Block one.\n\n\nBlock two."
        expected_blocks = ["Block one.", "Block two."]
        self.assertListEqual(markdown_to_blocks(markdown), expected_blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> quoted text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_single_line(self):
        block = "- item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi_line(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbers(self):
        block = "1. first\n3. third"
        # numbers wrong => should fall back to paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        block = "Just a regular paragraph.\nStill the same block."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestIsOrderedListBlock(unittest.TestCase):
    def test_valid_ordered_list(self):
        text = "1. one\n2. two\n3. three"
        self.assertTrue(is_ordered_list_block(text))

    def test_single_item_valid(self):
        text = "1. only"
        self.assertTrue(is_ordered_list_block(text))

    def test_starts_not_at_one(self):
        text = "2. two\n3. three"
        self.assertFalse(is_ordered_list_block(text))

    def test_non_consecutive_numbers(self):
        text = "1. one\n3. three"
        self.assertFalse(is_ordered_list_block(text))

    def test_not_a_list(self):
        text = "1. one\nnot a list line"
        self.assertFalse(is_ordered_list_block(text))

class TestMarkdownTOHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == '__main__':
    unittest.main()
