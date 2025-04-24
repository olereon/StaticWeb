# --- START OF FILE test_extract_title.py ---

import unittest

# Adjust import path if necessary
try:
    from htmlnode import extract_title
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust path
    from htmlnode import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_basic_h1(self):
        md = "# This is the Title"
        self.assertEqual(extract_title(md), "This is the Title")

    def test_h1_with_extra_whitespace(self):
        md = """
Some text before

#   My Title with Spaces

More text after.
"""
        self.assertEqual(extract_title(md), "My Title with Spaces")

    def test_h1_at_start(self):
        md = "# Start Title\nSome content"
        self.assertEqual(extract_title(md), "Start Title")

    def test_h1_at_end(self):
        md = "Some content\n# End Title"
        self.assertEqual(extract_title(md), "End Title")

    def test_no_h1(self):
        md = "This document has no H1.\n## But it has H2."
        with self.assertRaisesRegex(ValueError, "No H1 header found"):
            extract_title(md)

    def test_h2_present_no_h1(self):
        md = "## H2 Header\nSome content."
        with self.assertRaisesRegex(ValueError, "No H1 header found"):
            extract_title(md)

    def test_invalid_h1_no_space(self):
        md = "#Invalid H1\nContent."
        with self.assertRaisesRegex(ValueError, "No H1 header found"):
            extract_title(md) # Fails because it doesn't start with '# '

    def test_multiple_h1(self):
        # Function should return the *first* one found
        md = "Content\n# First Title\nMore Content\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_empty_input(self):
        md = ""
        with self.assertRaisesRegex(ValueError, "Cannot extract title from empty markdown"):
             extract_title(md)

    def test_none_input(self):
         # Function doesn't explicitly check for None, relies on split to fail
         # Let's test that it does fail appropriately
         with self.assertRaises(AttributeError): # split fails on None
             extract_title(None)


if __name__ == "__main__":
    unittest.main()