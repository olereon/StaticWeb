# --- START OF FILE test_markdown_extraction.py ---

import unittest

# Adjust import path if functions are in a different file/module
try:
    from htmlnode import extract_markdown_images, extract_markdown_links
except ImportError:
    # Handle cases where the script is run directly and modules are in the same dir
    import sys
    import os
    sys.path.append(os.path.dirname(__file__)) # Or adjust to your project structure
    from htmlnode import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):

    # --- Image Extraction Tests ---

    def test_extract_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_no_images(self):
        text = "This text has no images, but maybe a [link](https://example.com)."
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_empty_alt(self):
        text = "Image with empty alt ![](/path/to/image.jpg)"
        expected = [("", "/path/to/image.jpg")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_empty_url(self):
        # While maybe not valid markdown, the pattern should match
        text = "Image with empty URL ![alt text]()"
        expected = [("alt text", "")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_mixed_content(self):
        text = "![img1](url1) some text ![img2](url2) more text."
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertListEqual(extract_markdown_images(text), expected)

    def test_extract_images_adjacent(self):
        text = "![img1](url1)![img2](url2)"
        expected = [("img1", "url1"), ("img2", "url2")]
        self.assertListEqual(extract_markdown_images(text), expected)


    # --- Link Extraction Tests ---

    def test_extract_links_single(self):
        text = "Here is a [link to google](https://google.com)."
        expected = [("link to google", "https://google.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_no_links(self):
        text = "This text has no links, but maybe an ![image](https://example.com/img.png)."
        expected = []
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_empty_anchor(self):
        text = "Link with empty anchor [](/some/path)"
        expected = [("", "/some/path")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_empty_url(self):
        text = "Link with empty URL [anchor text]()"
        expected = [("anchor text", "")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_mixed_content(self):
        text = "[link1](url1) some text [link2](url2) more text."
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_adjacent(self):
        text = "[link1](url1)[link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_ignores_images(self):
        text = "This has a [real link](link.com) and an ![image link](image.com)."
        expected = [("real link", "link.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_mixed_links_and_images(self):
        text = "Link [one](1.com), then image ![alt](img.com), then link [two](2.com)."
        expected = [("one", "1.com"), ("two", "2.com")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_links_false_positive_brackets(self):
        text = "This text [contains brackets] but (not a link)."
        expected = []
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_extract_images_false_positive_brackets(self):
        text = "This text ![contains brackets] but (not an image)."
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)


if __name__ == "__main__":
    unittest.main()