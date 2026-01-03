import unittest
from markdown_blocks import markdown_to_blocks

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

if __name__ == '__main__':
    unittest.main()
