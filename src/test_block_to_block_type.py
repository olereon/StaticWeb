# --- START OF FILE test_block_to_block_type.py ---

import unittest

# Adjust import path if necessary
try:
    from htmlnode import block_to_block_type, BlockType
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust path
    from htmlnode import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # --- Paragraph Tests ---
    def test_paragraph_basic(self):
        block = "This is a standard paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This paragraph\nspans multiple\nlines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_heading_no_space(self):
        block = "#HeadingWithoutSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_code_missing_fence(self):
        block = "```\ncode here\n" # Missing closing fence
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block2 = "code here\n```" # Missing opening fence
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_quote_incomplete(self):
        block = "> Quote line 1\nThis line breaks the quote."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_ul_incomplete(self):
        block = "- Item 1\n* Item 2\nNot an item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_ol_incomplete(self):
        block = "1. First\n3. Third (breaks sequence)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_ol_wrong_format(self):
        block = "1) First\n2) Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # --- Heading Tests ---
    def test_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        block = "####### Not a Heading (too many hashes)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        block = "#Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # --- Code Block Tests ---
    def test_code_basic(self):
        block = "```\ndef main():\n  pass\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_empty(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_single_line(self):
        block = "```print('hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_missing_closing_fence(self):
        block = "```\nprint('hello')\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_missing_opening_fence(self):
        block = "print('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    # --- Quote Block Tests ---
    def test_quote_single_line(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> First line.\n> Second line.\n> Third line."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_missing_marker_on_one_line(self):
        block = "> First line.\nSecond line breaks it.\n> Third line."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_with_spaces_after_marker(self):
        # Assumes '>' is enough, spaces are part of the line content
        block = ">  Spaces after marker.\n> Another line."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)


    # --- Unordered List Tests ---
    def test_ul_stars(self):
        block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ul_dashes(self):
        block = "- Item A\n- Item B"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ul_mixed_markers(self):
        # Function currently requires *all* lines to match EITHER pattern
        # Standard markdown might treat this differently, but per the simple rule:
        block = "* Item 1\n- Item B"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ul_missing_marker_on_one_line(self):
        block = "* Item 1\nItem 2 breaks it."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ul_missing_space(self):
        block = "*Item 1\n*Item 2" # Missing space after '*'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block2 = "-Item A\n-Item B" # Missing space after '-'
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)


    # --- Ordered List Tests ---
    def test_ol_basic(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ol_single_item(self):
        block = "1. Only one item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ol_sequence_broken(self):
        block = "1. First\n3. Third (skips 2)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ol_starts_wrong(self):
        block = "2. Starts at 2\n3. Continues"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block0 = "0. Starts at 0"
        self.assertEqual(block_to_block_type(block0), BlockType.PARAGRAPH)

    def test_ol_wrong_format(self):
        block = "1) Wrong format\n2) Another"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block_no_dot = "1 No dot\n2 No dot"
        self.assertEqual(block_to_block_type(block_no_dot), BlockType.PARAGRAPH)
        block_no_space = "1.No space\n2.No space"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.PARAGRAPH)

    def test_ol_large_numbers(self):
        block = "1. One\n2. Two\n3. Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()