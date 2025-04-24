# --- START OF FILE test_markdown_to_blocks.py ---

import unittest

# Adjust import path if necessary
try:
    from htmlnode import markdown_to_blocks
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust path
    from htmlnode import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_split(self):
        md = """
Block 1

Block 2
continues here.

Block 3
"""
        expected = [
            "Block 1",
            "Block 2\ncontinues here.",
            "Block 3"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_example_from_prompt(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_multiple_newlines(self):
        md = "Block A\n\n\n\nBlock B\n\nBlock C"
        expected = [
            "Block A",
            "Block B",
            "Block C"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace_document(self):
        md = "   \n\nBlock Alpha\n\n  Block Beta  \n\n   "
        expected = [
            "Block Alpha",
            "Block Beta"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace_blocks(self):
        # Strip should remove whitespace *around* blocks, but not *within* lines
        md = "  Leading space block 1.\nLine 2 of block 1.   \n\n  Block 2 Line 1 \n  Block 2 Line 2  "
        expected = [
            "Leading space block 1.\nLine 2 of block 1.",
            "Block 2 Line 1 \n  Block 2 Line 2" # Internal leading/trailing space on lines is kept
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_single_block(self):
        md = "This is just\none single block."
        expected = [
            "This is just\none single block."
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_empty_input(self):
        md = ""
        expected = []
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_only_whitespace_input(self):
        md = "   \n \n  \n\n \t \n\n  "
        expected = []
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_no_double_newlines(self):
        md = "Line 1\nLine 2\nLine 3"
        expected = [
            "Line 1\nLine 2\nLine 3"
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_none_input(self):
        md = None
        expected = []
        self.assertListEqual(markdown_to_blocks(md), expected)

    def test_mixed_whitespace_newlines(self):
        md = "Block 1\n \n Block 2\n\n\n   Block 3 \n\t\nBlock 4"
        expected = [
            "Block 1\n \n Block 2", # Whitespace line preserved within block
            "Block 3 \n\t\nBlock 4" # Tabs/newlines preserved within block
        ]
        self.assertListEqual(markdown_to_blocks(md), expected)


if __name__ == "__main__":
    unittest.main()