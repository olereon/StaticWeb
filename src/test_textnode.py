import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        # Test equality when both nodes have the same URL
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
    
    def test_eq_with_none_url(self):
        # Test equality when both nodes have None URL (default value)
        node = TextNode("Plain text", TextType.TEXT)
        node2 = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(node, node2)
        
        # Explicitly set None URL
        node3 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node3)
    
    def test_not_eq_different_text(self):
        # Test inequality when text values are different
        node = TextNode("First text", TextType.TEXT)
        node2 = TextNode("Second text", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_different_text_type(self):
        # Test inequality when text_type values are different
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_different_url(self):
        # Test inequality when URL values are different
        node = TextNode("Same link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Same link text", TextType.LINK, "https://another-example.com")
        self.assertNotEqual(node, node2)
        
        # Test inequality when one URL is None and the other isn't
        node3 = TextNode("Same link text", TextType.LINK)  # None URL
        self.assertNotEqual(node, node3)


if __name__ == "__main__":
    unittest.main()