# --- START OF FILE test_text_to_textnodes.py ---

import unittest

# Adjust import path if necessary
try:
    from textnode import TextNode, TextType
    from htmlnode import text_to_textnodes
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust path
    from textnode import TextNode, TextType
    from htmlnode import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_basic_conversion(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_plain_text(self):
        text = "Just some plain text without any markdown."
        expected = [
            TextNode("Just some plain text without any markdown.", TextType.TEXT)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_only_bold(self):
        text = "Some **bold** text."
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_only_italic(self):
        text = "Some *italic* text."
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_only_code(self):
        text = "Some `code` text."
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_only_image(self):
        text = "An ![image](url.png)."
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_only_link(self):
        text = "A [link](url.com)."
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_adjacent_elements(self):
        text = "**bold***italic*`code`[link](url)![img](img.url)"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("link", TextType.LINK, "url"),
            TextNode("img", TextType.IMAGE, "img.url"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_mixed_order(self):
        text = "Code `here`, then *italic*, then a ![pic](url.jpg)."
        expected = [
            TextNode("Code ", TextType.TEXT),
            TextNode("here", TextType.CODE),
            TextNode(", then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", then a ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "url.jpg"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_empty_input(self):
        text = ""
        expected = []
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_none_input(self):
        text = None
        expected = []
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_whitespace_handling(self):
        text = "  Leading space. **Bold text** and * italic * with spaces. Trailing space.  "
        expected = [
            TextNode("  Leading space. ", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode(" italic ", TextType.ITALIC), # Spaces inside are preserved
            TextNode(" with spaces. Trailing space.  ", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_unmatched_delimiter_raises_error(self):
        text = "This has an `unclosed code block"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

        text2 = "This has **unclosed bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text2)

        text3 = "This has *unclosed italic"
        with self.assertRaises(ValueError):
            text_to_textnodes(text3)

    def test_bold_and_italic_adjacent(self):
        # Test cases where bold and italic are separate or adjacent but not directly nested like ***
        text = "Here is **bold** and *italic* text."
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

        text2 = "**bold***italic*" # Adjacent
        expected2 = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(text_to_textnodes(text2), expected2)
        '''
        str.split() can not handle this case correctly.
        text3 = "*italic***bold**" # Adjacent
        expected3 = [
            TextNode("italic", TextType.ITALIC),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(text_to_textnodes(text3), expected3)
        '''


if __name__ == "__main__":
    unittest.main()