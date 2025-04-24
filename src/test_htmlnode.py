import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        # Test with multiple properties
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty_props(self):
        # Test with empty props dictionary
        node = HTMLNode(tag="p", value="Hello, world!", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props(self):
        # Test with None props
        node = HTMLNode(tag="div", value="Content")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        # Test the __repr__ method
        node = HTMLNode(
            tag="img",
            props={"src": "image.jpg", "alt": "An image"}
        )
        expected = 'HTMLNode(tag=img, value=None, children=None, props={\'src\': \'image.jpg\', \'alt\': \'An image\'})'
        self.assertEqual(repr(node), expected)

    def test_initialization_defaults(self):
        # Test default initialization values
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a_with_props(self):
        node = LeafNode(
            "a", 
            "Click me!", 
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com" target="_blank">Click me!</a>'
        )
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
        
    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Styled text", {})
        self.assertEqual(node.to_html(), "<span>Styled text</span>")
        
    def test_leaf_node_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
            
    def test_leaf_node_no_children(self):
        node = LeafNode("div", "Content")
        self.assertIsNone(node.children)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
        
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )
        
    def test_to_html_complex_nesting(self):
        # Create a complex nested structure
        text1 = LeafNode(None, "Hello ")
        bold = LeafNode("b", "bold")
        text2 = LeafNode(None, " and ")
        italic = LeafNode("i", "italic")
        text3 = LeafNode(None, " world!")
        
        span = ParentNode("span", [text1, bold, text2, italic, text3])
        div = ParentNode("div", [span], {"class": "content"})
        
        self.assertEqual(
            div.to_html(),
            '<div class="content"><span>Hello <b>bold</b> and <i>italic</i> world!</span></div>',
        )
        
    def test_parent_node_no_tag_raises_error_init(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")])
            
    def test_parent_node_no_children_raises_error_init(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
            
    def test_parent_node_empty_children_list(self):
        # Empty list is valid (though not very useful)
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
        
    def test_parent_node_nested_parent_nodes(self):
        inner1 = ParentNode("div", [LeafNode("span", "inner1")])
        inner2 = ParentNode("div", [LeafNode("span", "inner2")])
        outer = ParentNode("section", [inner1, inner2])
        
        self.assertEqual(
            outer.to_html(),
            "<section><div><span>inner1</span></div><div><span>inner2</span></div></section>",
        )
        
    def test_parent_node_with_mixed_node_types(self):
        text = LeafNode(None, "Text between elements")
        child1 = LeafNode("h1", "Heading")
        child2 = ParentNode("ul", [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
        ])
        
        parent = ParentNode("div", [child1, text, child2])
        
        self.assertEqual(
            parent.to_html(),
            "<div><h1>Heading</h1>Text between elements<ul><li>Item 1</li><li>Item 2</li></ul></div>",
        )

if __name__ == "__main__":
    unittest.main()