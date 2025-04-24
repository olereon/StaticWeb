# --- START OF FILE test_split_nodes_image_link.py ---

import unittest

# Adjust import path if necessary
try:
    from textnode import TextNode, TextType
    from htmlnode import split_nodes_image, split_nodes_link
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust path
    from textnode import TextNode, TextType
    from htmlnode import split_nodes_image, split_nodes_link


class TestSplitNodesImageLink(unittest.TestCase):

    # --- Image Splitting Tests ---

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_multiple(self):
        node = TextNode(
            "Text ![img1](url1) and ![img2](url2) end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_at_start(self):
        node = TextNode("![image](url) starts here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" starts here.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_at_end(self):
        node = TextNode("Ends here ![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Ends here ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_only_image(self):
        node = TextNode("![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_adjacent(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Just plain text.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_mixed_nodes_input(self):
        nodes = [
            TextNode("Before image", TextType.TEXT),
            TextNode("![img](url)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("After image", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Before image", TextType.TEXT), # Unchanged (no image inside)
            TextNode("img", TextType.IMAGE, "url"),   # Split
            TextNode("Bold text", TextType.BOLD),     # Unchanged (not TEXT)
            TextNode("After image", TextType.TEXT),  # Unchanged (no image inside)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_empty_text_node(self):
         nodes = [TextNode("", TextType.TEXT)]
         new_nodes = split_nodes_image(nodes)
         self.assertListEqual(new_nodes, []) # Should return empty list

    def test_split_images_with_empty_alt(self):
        node = TextNode("Image ![](/url) here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "/url"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)


    # --- Link Splitting Tests ---

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a [link](https://example.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_multiple(self):
        node = TextNode(
            "Text [link1](url1) and [link2](url2) end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_at_start(self):
        node = TextNode("[link](url) starts here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" starts here.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_at_end(self):
        node = TextNode("Ends here [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Ends here ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_only_link(self):
        node = TextNode("[link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_adjacent(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_no_links(self):
        node = TextNode("Just plain text with ![image](img.png).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Just plain text with ![image](img.png).", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_mixed_nodes_input(self):
        nodes = [
            TextNode("Before link", TextType.TEXT),
            TextNode("[link](url)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("After link", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Before link", TextType.TEXT),   # Unchanged (no link inside)
            TextNode("link", TextType.LINK, "url"),   # Split
            TextNode("Italic text", TextType.ITALIC), # Unchanged (not TEXT)
            TextNode("After link", TextType.TEXT),   # Unchanged (no link inside)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_ignores_images_in_text(self):
         node = TextNode("Text with ![image](img.url) and [link](link.url).", TextType.TEXT)
         new_nodes = split_nodes_link([node])
         expected = [
             TextNode("Text with ![image](img.url) and ", TextType.TEXT),
             TextNode("link", TextType.LINK, "link.url"),
             TextNode(".", TextType.TEXT),
         ]
         self.assertListEqual(new_nodes, expected)

    def test_split_images_ignores_links_in_text(self):
         node = TextNode("Text with [link](link.url) and ![image](img.url).", TextType.TEXT)
         new_nodes = split_nodes_image([node])
         expected = [
             TextNode("Text with [link](link.url) and ", TextType.TEXT),
             TextNode("image", TextType.IMAGE, "img.url"),
             TextNode(".", TextType.TEXT),
         ]
         self.assertListEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()