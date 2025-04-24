import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, text_node_to_html_node


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")
    
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")
    
    def test_code(self):
        node = TextNode("let x = 10;", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "let x = 10;")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<code>let x = 10;</code>")
    
    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">Click me</a>')
    
    def test_link_missing_url(self):
        node = TextNode("Click me", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
    
    def test_image(self):
        node = TextNode("Sample image", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "Sample image"})
        self.assertEqual(html_node.to_html(), '<img src="image.jpg" alt="Sample image"></img>')
    
    def test_image_missing_url(self):
        node = TextNode("Sample image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()