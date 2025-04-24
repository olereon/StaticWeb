# --- START OF FILE test_split_nodes_delimiter.py ---

import unittest

# Assuming TextNode and TextType are in a sibling 'textnode' module
# Adjust the import path if your structure is different
try:
    from textnode import TextNode, TextType
    from htmlnode import split_nodes_delimiter
except ImportError:
    # Handle cases where the script is run directly and modules are in the same dir
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from textnode import TextNode, TextType
    from htmlnode import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_italic(self):
        node = TextNode("This has *italic* text", TextType.TEXT) # Using '*' for italic common markdown
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_multiple_same_type(self):
        node = TextNode("*italic1* plain *italic2*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("italic1", TextType.ITALIC),
            TextNode(" plain ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_no_delimiters(self):
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Plain text without delimiters", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("text at the end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("text at the end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_multiple_nodes_input(self):
        # This tests processing multiple nodes, but only one delimiter type at a time
        node1 = TextNode("Text with `code`", TextType.TEXT)
        node2 = TextNode("Just plain text.", TextType.TEXT)
        node3 = TextNode("Another `code` example.", TextType.TEXT)
        nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Just plain text.", TextType.TEXT), # node2 is unchanged
            TextNode("Another ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" example.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_empty_content_between_delimiters(self):
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            # Empty string between delimiters is skipped by the loop
            TextNode(" empty code", TextType.TEXT),
        ]
        # Correction: The split " `` " results in ["", "", " empty code"] which has length 3 (odd).
        # The middle empty string *should* become a node if we want to represent ``.
        # Let's refine the function slightly to allow empty nodes if needed.
        # --- Re-Refining the function based on this test ---
        # We need to decide if `` should result in TextNode("", TextType.CODE) or be skipped.
        # Markdown usually allows empty emphasis like ****. Let's allow it.
        # The `if not part: continue` should be removed or modified.
        # Let's modify the function again to handle this.

        # --- Second Refinement of `split_nodes_delimiter` (allowing empty content) ---
        # (Modify the loop in the function)
        # for i, part in enumerate(split_parts):
        #     # Don't skip empty parts entirely, just handle TEXT vs delimited type
        #     if i % 2 == 0:
        #         if part: # Only add non-empty text nodes
        #             new_nodes.append(TextNode(part, TextType.TEXT))
        #     else:
        #         # Allow empty delimited nodes (e.g. `` becomes code node with "")
        #         new_nodes.append(TextNode(part, text_type))

        # --- Now, the expected result for this test changes ---
        expected_refined = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("", TextType.CODE), # Empty code node
            TextNode(" empty code", TextType.TEXT),
        ]
        # Rerun with the refined function logic (assuming function is updated)
        # Need to simulate the update here for the test expectation:
        self.assertListEqual(new_nodes, expected_refined) # Use this expectation with refined func

    def test_raises_error_unmatched_delimiter(self):
        # Test that an unmatched delimiter raises ValueError
        node = TextNode("Text with `unclosed code block", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: Unmatched closing delimiter"):
            split_nodes_delimiter([node], "`", TextType.CODE)

        node_start = TextNode("`unclosed at start", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: Unmatched closing delimiter"):
            split_nodes_delimiter([node_start], "`", TextType.CODE)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Plain text", TextType.TEXT),
            TextNode("Link node", TextType.LINK, "https://example.com"),
            TextNode("Image node", TextType.IMAGE, "img.png"),
            TextNode("Bold node", TextType.BOLD), # Already bold, should not be split by '*'
            TextNode("More *italic* text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Plain text", TextType.TEXT), # Unchanged
            TextNode("Link node", TextType.LINK, "https://example.com"), # Unchanged
            TextNode("Image node", TextType.IMAGE, "img.png"), # Unchanged
            TextNode("Bold node", TextType.BOLD), # Unchanged
            # Last node is split:
            TextNode("More ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_empty_input_list(self):
        self.assertListEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_only_non_text_nodes_input(self):
        nodes = [
            TextNode("Link", TextType.LINK, "/"),
            TextNode("Image", TextType.IMAGE, "img.jpg")
        ]
        self.assertListEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), nodes) # Should return the same list

    def test_consecutive_delimiters(self):
        # Test case: `code1``code2`
        node = TextNode("Text `code1``code2` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Splits into: ["Text ", "code1", "", "code2", " more text"] (len 5 - OK)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("", TextType.CODE),      # Middle empty part becomes CODE
            TextNode("code2", TextType.CODE),
            TextNode(" more text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

        # Test case: **bold1****bold2**
        node2 = TextNode("**bold1****bold2**", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        # Splits into: ["", "bold1", "", "bold2", ""] (len 5 - OK)
        expected2 = [
            # First "" is skipped because it's TEXT
            TextNode("bold1", TextType.BOLD),
            TextNode("", TextType.BOLD), # Middle "" becomes BOLD
            TextNode("bold2", TextType.BOLD),
            # Last "" is skipped because it's TEXT
        ]
        self.assertListEqual(new_nodes2, expected2)

    def test_delimiter_itself_as_text(self):
        # Ensure delimiters not matching the type are preserved
        node = TextNode("Text with `code` and *italic*", TextType.TEXT)
        # Split by CODE first
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and *italic*", TextType.TEXT), # *italic* remains as text
        ]
        self.assertListEqual(new_nodes, expected)

        # Now split the result by ITALIC
        final_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected_final = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE), # Remains CODE
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC), # Now split
            TextNode("", TextType.TEXT), # Will be skipped by refined function
        ]
        # Adjusting expected_final based on function refinement (empty TEXT nodes skipped)
        expected_final_refined = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE), # Remains CODE
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC), # Now split
        ]
        self.assertListEqual(final_nodes, expected_final_refined)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # Use exit=False if running in interactive env like Jupyter