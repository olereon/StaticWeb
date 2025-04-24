# --- In htmlnode.py ---
import re
import os # Add os import if not already present
import shutil # Add shutil import if not already present
from textnode import TextNode, TextType, BlockType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        
        return props_string

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Call the parent constructor but force children to be None
        super().__init__(tag=tag, value=value, children=None, props=props)
        
        # Ensure value is provided
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        # If there's no tag, just return the value as raw text
        if self.tag is None:
            return self.value
            
        # Otherwise, render as HTML tag with props
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Call the parent constructor with value=None and the provided arguments
        super().__init__(tag=tag, value=None, children=children, props=props)
        
        # Ensure tag is provided
        if tag is None:
            raise ValueError("ParentNode must have a tag")
            
        # Ensure children is provided
        if children is None:
            raise ValueError("ParentNode must have children")

    def to_html(self):
        # If there's no tag, raise an error
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
            
        # If there are no children, raise an error
        if self.children is None:
            raise ValueError("ParentNode must have children")
            
        # Generate the HTML for all children
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        # Return the parent tag wrapping the children HTML
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
    

def copy_directory_recursive(source_path, destination_path):
    """
    Recursively copies all files and directories from source_path
    to destination_path.

    Args:
        source_path (str): The path to the source directory.
        destination_path (str): The path to the destination directory.
    """
    # print(f"Copying contents from '{source_path}' to '{destination_path}'") # Optional: Log entering directory

    # Ensure the destination directory exists for this level
    if not os.path.exists(destination_path):
        print(f"  Creating destination directory: '{destination_path}'")
        os.mkdir(destination_path)
    elif not os.path.isdir(destination_path):
         # Raise an error if the destination exists but is not a directory
         raise NotADirectoryError(f"Destination path exists but is not a directory: {destination_path}")


    # Iterate through items in the source directory
    if not os.path.exists(source_path):
         raise FileNotFoundError(f"Source directory not found: {source_path}")

    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)

        if os.path.isfile(source_item_path):
            print(f"  Copying file: '{source_item_path}' -> '{destination_item_path}'")
            shutil.copy(source_item_path, destination_item_path)
        elif os.path.isdir(source_item_path):
            # Recursive call for subdirectory
            copy_directory_recursive(source_item_path, destination_item_path)
        # else: Could handle other types like symlinks if needed
    
def extract_title(markdown: str) -> str:
    """
    Extracts the text content of the first H1 header (line starting with '# ')
    from a markdown string.

    Args:
        markdown: The raw markdown string.

    Returns:
        The text content of the H1 header.

    Raises:
        ValueError: If no H1 header is found or if markdown is empty.
        AttributeError: If markdown input is None.
    """
    # Let the AttributeError happen naturally if input is None
    # Then check for empty string if it's not None
    if markdown == "": # Check specifically for empty string
        raise ValueError("Cannot extract title from empty markdown")

    lines = markdown.split('\n') # This will raise AttributeError if markdown is None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('# '):
            return stripped_line[2:].strip()

    raise ValueError("No H1 header found in markdown content")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    """
    Recursively generates HTML pages from markdown files in a source directory.

    Scans the dir_path_content, finds all '.md' files, generates HTML using
    the template_path, and writes the output to dest_dir_path, preserving
    the directory structure.

    Args:
        dir_path_content: Path to the source content directory.
        template_path: Path to the HTML template file.
        dest_dir_path: Path to the destination directory for generated HTML files.
    """
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Content source directory not found: {dir_path_content}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    print(f"Scanning content directory: {dir_path_content}")

    for item in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item)
        # Construct the potential destination path equivalent
        dest_item_path_equivalent = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_item_path):
            if item.endswith(".md"):
                # Change extension for the final destination path
                # Using os.path.splitext for robustness
                base_name, _ = os.path.splitext(item)
                html_dest_path = os.path.join(dest_dir_path, base_name + ".html")

                print(f"  Generating page for: {source_item_path} -> {html_dest_path}")
                try:
                    # Call the single-page generation function
                    generate_page(source_item_path, template_path, html_dest_path)
                except Exception as e:
                    # Log errors but continue processing other files/dirs
                    print(f"    ERROR generating page for '{source_item_path}': {e}")
            else:
                # Optional: Could copy other files here if needed, but assignment focuses on MD->HTML
                # print(f"  Skipping non-markdown file: {source_item_path}")
                pass
        elif os.path.isdir(source_item_path):
            # Ensure the corresponding destination directory exists
            print(f"  Entering directory: {source_item_path}")
            # No need to explicitly create dest_item_path_equivalent here,
            # os.makedirs in generate_page handles leaf directories.
            # And listdir needs the source dir, not dest dir, to exist.
            # The destination path for the *next level* is handled by the recursive call.
            # Recursive call
            generate_pages_recursive(
                source_item_path,       # Source is the subdirectory
                template_path,          # Template remains the same
                dest_item_path_equivalent # Destination is the corresponding subdirectory
            )

#'''
def generate_page(from_path: str, template_path: str, dest_path: str):
    """
    Generates an HTML page from a markdown file using a template.

    Reads markdown from from_path, converts it to HTML, extracts the title,
    reads the template from template_path, replaces placeholders, and writes
    the final HTML to dest_path.

    Args:
        from_path: Path to the source markdown file.
        template_path: Path to the HTML template file.
        dest_path: Path where the generated HTML file will be saved.
    """
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    # 1. Read markdown file
    try:
        with open(from_path, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Markdown file not found: {from_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading markdown file {from_path}: {e}")

    # 2. Read template file
    try:
        with open(template_path, 'r', encoding='utf-8') as tmpl_file:
            template_content = tmpl_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading template file {template_path}: {e}")

    # 3. Convert markdown to HTML
    try:
        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()
    except Exception as e:
        # Catch potential errors from markdown parsing (e.g., invalid syntax)
        raise RuntimeError(f"Error converting markdown to HTML from {from_path}: {e}")


    # 4. Extract title
    try:
        title = extract_title(markdown_content)
    except ValueError as e:
        # Propagate the error if title is missing
        raise ValueError(f"Could not extract title from {from_path}: {e}")

    # 5. Replace placeholders
    if "{{ Title }}" not in template_content:
         print(f"Warning: '{{{{ Title }}}}' placeholder not found in template: {template_path}")
    if "{{ Content }}" not in template_content:
         print(f"Warning: '{{{{ Content }}}}' placeholder not found in template: {template_path}")

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # 6. Write the new HTML to dest_path
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir: # Only create if dirname is not empty (i.e., not root dir)
        os.makedirs(dest_dir, exist_ok=True)

    try:
        with open(dest_path, 'w', encoding='utf-8') as out_file:
            out_file.write(final_html)
    except Exception as e:
        raise RuntimeError(f"Error writing HTML file to {dest_path}: {e}")
#'''

def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL cannot be None for LINK type TextNode")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL cannot be None for IMAGE type TextNode")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNodes of type TEXT based on a given delimiter.

    Args:
        old_nodes (list[TextNode]): The list of nodes to process.
        delimiter (str): The delimiter string (e.g., "`", "**", "_").
        text_type (TextType): The TextType to apply to text between delimiters.

    Returns:
        list[TextNode]: A new list of nodes with TEXT nodes potentially split.

    Raises:
        ValueError: If an unmatched closing delimiter is found.
    """
    new_nodes = []
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Skip processing if the text node is empty
        if not old_node.text:
            continue

        # Split the text of the current node by the delimiter
        sections = old_node.text.split(delimiter)

        #print(f"  [SPLIT RESULT] For text '{old_node.text}' with delimiter '{delimiter}', split produced: {sections}")

        # If only one part, the delimiter wasn't found
        if len(sections) == 1:
            # Append the original node since no splitting occurred
            new_nodes.append(old_node)
            continue

        # Validate that delimiters are paired (must be an odd number of parts)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched closing delimiter '{delimiter}' in text: '{old_node.text}'")

        # Process the split sections
        for i, section in enumerate(sections):
            is_inside_delimiters = (i % 2 != 0)

            # --- ADD MORE DEBUGGING ---
            #print(f"  [SPLIT DEBUG] i={i}, section='{section}', is_inside={is_inside_delimiters}")
            # --- / ADD MORE DEBUGGING ---

            if is_inside_delimiters:
                # print(f"    -> Creating Node: TextNode('{section}', {text_type})") # DEBUG
                new_nodes.append(TextNode(section, text_type))
            else:
                is_empty_from_adjacent_delimiters = (section == "" and i > 0 and i < len(sections) - 1)
                if is_empty_from_adjacent_delimiters:
                    #print(f"    -> Creating Node (adjacent empty): TextNode('', {text_type})") # DEBUG
                     new_nodes.append(TextNode("", text_type))
                elif section:
                    #print(f"    -> Creating Node: TextNode('{section}', {TextType.TEXT})") # DEBUG
                    new_nodes.append(TextNode(section, TextType.TEXT))
                #else:
                    #print(f"    -> Skipping empty section at i={i}") # DEBUG

    return new_nodes

def extract_markdown_images(text):
    """
    Extracts markdown image links from text.

    Args:
        text (str): The raw markdown text.

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple contains
                                the alt text and the URL of an image.
                                e.g., [("alt text", "url"), ...]
    """
    # Pattern: ![alt text](url)
    # - \!\[ : Matches the literal '!['
    # - (.*?) : Captures the alt text (non-greedy)
    # - \] : Matches the literal ']'
    # - \( : Matches the literal '('
    # - (.*?) : Captures the URL (non-greedy)
    # - \) : Matches the literal ')'
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown links from text (excluding image links).

    Args:
        text (str): The raw markdown text.

    Returns:
        list[tuple[str, str]]: A list of tuples, where each tuple contains
                                the anchor text and the URL of a link.
                                e.g., [("anchor text", "url"), ...]
    """
    # Pattern: [anchor text](url) but NOT preceded by !
    # - (?<!\!) : Negative lookbehind - asserts that '!' does not precede
    # - \[ : Matches the literal '['
    # - (.*?) : Captures the anchor text (non-greedy)
    # - \] : Matches the literal ']'
    # - \( : Matches the literal '('
    # - (.*?) : Captures the URL (non-greedy)
    # - \) : Matches the literal ')'
    # Note: We need to find non-image links. The lookbehind (?<!\!) ensures
    # that we only match patterns like '[text](url)' that are NOT immediately
    # preceded by a '!'.
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    """
    Splits TEXT nodes based on Markdown image syntax ![alt](url).

    Args:
        old_nodes (list[TextNode]): A list of nodes to process.

    Returns:
        list[TextNode]: A new list with TEXT nodes split by images.
    """
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        # Skip empty text nodes
        if not original_text:
            continue

        # Extract all images from the node's text
        images = extract_markdown_images(original_text)

        # If no images, add the original node (if it has text) and continue
        if not images:
            new_nodes.append(old_node)
            continue

        # Start with the full text as the part to process
        remaining_text = original_text
        for img_alt, img_url in images:
            # Construct the full Markdown string for the current image
            md_image = f"![{img_alt}]({img_url})"

            # Split the *remaining* text segment at the first occurrence of this image
            parts = remaining_text.split(md_image, 1)

            # If split didn't work (e.g., text somehow changed), skip adding parts for safety
            # but this shouldn't happen if extract_markdown_images worked correctly.
            if len(parts) < 2:
                 # If the remaining text *is* the image, parts will be ['', '']
                 if remaining_text != md_image:
                     # Log or raise error? For now, just break processing this node if inconsistent
                     print(f"Warning: Could not split text '{remaining_text}' on image '{md_image}'")
                     # Add whatever was left as plain text? Or just stop?
                     # Let's add the problematic remaining text as-is and stop for this node.
                     if remaining_text:
                        new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                     remaining_text = "" # Prevent adding it again later
                     break # Stop processing images for this node

            # Get the text before the image
            text_before = parts[0]
            if text_before: # Don't add empty strings
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            # Add the image node itself
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))

            # Update remaining_text to the part *after* this image for the next iteration
            remaining_text = parts[1]

        # After the loop, if there's any text left over, add it as a text node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits TEXT nodes based on Markdown link syntax [text](url).

    Args:
        old_nodes (list[TextNode]): A list of nodes to process.

    Returns:
        list[TextNode]: A new list with TEXT nodes split by links.
    """
    new_nodes = []
    for old_node in old_nodes:
        # Skip non-TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        # Skip empty text nodes
        if not original_text:
            continue

        # Extract all links from the node's text
        links = extract_markdown_links(original_text)

        # If no links, add the original node (if it has text) and continue
        if not links:
            new_nodes.append(old_node)
            continue

        # Start with the full text as the part to process
        remaining_text = original_text
        for link_text, link_url in links:
            # Construct the full Markdown string for the current link
            md_link = f"[{link_text}]({link_url})"

            # Split the *remaining* text segment at the first occurrence of this link
            parts = remaining_text.split(md_link, 1)

            # If split didn't work (shouldn't normally happen)
            if len(parts) < 2:
                 if remaining_text != md_link:
                     print(f"Warning: Could not split text '{remaining_text}' on link '{md_link}'")
                     if remaining_text:
                         new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                     remaining_text = ""
                     break # Stop processing links for this node

            # Get the text before the link
            text_before = parts[0]
            if text_before: # Don't add empty strings
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            # Add the link node itself
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # Update remaining_text to the part *after* this link for the next iteration
            remaining_text = parts[1]

        # After the loop, if there's any text left over, add it as a text node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    """
    Converts a raw string with markdown into a list of TextNode objects,
    supporting both * and _ for italics.
    """
    if text is None:
        return []
    if not text:
        return []

    nodes = [TextNode(text, TextType.TEXT)]

    # Apply splitters in order
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # --- ADDED/MODIFIED FOR ITALICS ---
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) # Process * italics
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) # Process _ italics
    # --- / ADDED/MODIFIED FOR ITALICS ---
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits a raw markdown string document into a list of block strings.

    Blocks are separated by 2 or more newline characters. Leading and
    trailing whitespace is removed from each block, and blocks consisting
    only of whitespace (or empty after stripping) are omitted.

    Args:
        markdown: The raw markdown string document.

    Returns:
        A list of strings, where each string is a block of markdown.
        Returns an empty list if the input is None.
    """
    if markdown is None:
        return []

    # Split the document by two or more newline characters
    # This handles cases with \n\n, \n\n\n, etc.
    potential_blocks = markdown.split('\n\n')

    # Clean up each block and filter out empty ones
    final_blocks = []
    for block in potential_blocks:
        # Remove leading/trailing whitespace (including potential stray newlines)
        cleaned_block = block.strip()
        # Only add the block if it's not empty after stripping
        if cleaned_block:
            final_blocks.append(cleaned_block)

    return final_blocks

def block_to_block_type(block: str) -> BlockType:
    """Determines the BlockType of a given markdown block string.

    Assumes leading/trailing whitespace has been stripped from the block.

    Args:
        block: A single string representing a block of markdown text.

    Returns:
        The BlockType enum member representing the block's type.
    """
    # --- Heading Check ---
    # Use regex for flexibility: matches 1-6 '#' followed by a space at the start
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING

    # --- Code Block Check ---
    # Must start and end with ```
    if block.startswith('```') and block.endswith('```'):
        # Basic check, assumes no escaped backticks complicate things
        return BlockType.CODE

    # Split block into lines for multi-line checks
    lines = block.split('\n')
    if not lines: # Should not happen if block isn't empty, but good check
        return BlockType.PARAGRAPH

    # --- Quote Block Check ---
    # Every line must start with '>'
    is_quote = all(line.startswith('>') for line in lines)
    if is_quote:
        return BlockType.QUOTE

    # --- Unordered List Check ---
    # Every line must start with '* ' or '- '
    is_ul = all(line.startswith('* ') or line.startswith('- ') for line in lines)
    if is_ul:
        return BlockType.UNORDERED_LIST

    # --- Ordered List Check ---
    # Every line must start with 'i. ' where i increments starting from 1
    is_ol = True
    expected_num = 1
    for line in lines:
        if not line.startswith(f'{expected_num}. '):
            is_ol = False
            break
        expected_num += 1
    if is_ol:
        return BlockType.ORDERED_LIST

    # --- Paragraph (Default) ---
    # If none of the above conditions are met
    return BlockType.PARAGRAPH

# --- In htmlnode.py ---
# ... (keep existing imports and code including text_to_textnodes, text_node_to_html_node) ...

def text_to_children(text: str) -> list[HTMLNode]:
    """Converts text with inline markdown into a list of HTMLNode children.

    Args:
        text: The raw text string potentially containing inline markdown.

    Returns:
        A list of HTMLNode objects (usually LeafNode) representing the parsed text.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts a full markdown document string into a parent HTMLNode.

    Args:
        markdown: The raw markdown string document.

    Returns:
        A single ParentNode ("div") containing children HTMLNodes
        representing the parsed markdown document.
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            # Determine level and extract text
            level = 0
            while block[level] == '#':
                level += 1
            # Ensure there's a space after hashes and text exists
            if level < len(block) and block[level] == ' ':
                 text_content = block[level + 1:].strip()
                 children = text_to_children(text_content)
                 block_nodes.append(ParentNode(f"h{level}", children))
            else: # Treat as paragraph if format is wrong (e.g. #NoSpace)
                 children = text_to_children(block) # Parse the original block text
                 block_nodes.append(ParentNode("p", children))


        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            block_nodes.append(ParentNode("p", children))

        elif block_type == BlockType.CODE:
            # Remove fences, treat content as plain text
            # Strip leading/trailing newlines often present inside fences
            code_content = block.strip("```").strip('\n')
            # Create LeafNode for code, wrap in ParentNode for pre
            code_leaf = LeafNode("code", code_content)
            block_nodes.append(ParentNode("pre", [code_leaf]))

        elif block_type == BlockType.QUOTE:
            # Process lines, remove '>', join, then parse inline
            lines = block.split('\n')
            processed_lines = []
            for line in lines:
                # Remove '>' and optional leading space
                cleaned_line = line.lstrip('>').lstrip()
                processed_lines.append(cleaned_line)
            quote_content = "\n".join(processed_lines)
            children = text_to_children(quote_content)
            block_nodes.append(ParentNode("blockquote", children))

        elif block_type == BlockType.UNORDERED_LIST:
            list_item_nodes = []
            lines = block.split('\n')
            for line in lines:
                # Remove marker ('* ' or '- ') and parse inline content
                # Slice from index 2 assuming marker is always 2 chars
                item_content = line[2:]
                children = text_to_children(item_content)
                list_item_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", list_item_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            list_item_nodes = []
            lines = block.split('\n')
            for line in lines:
                # Find the position of '. ' and slice after it
                marker_end_pos = line.find(". ")
                if marker_end_pos != -1:
                    item_content = line[marker_end_pos + 2:]
                    children = text_to_children(item_content)
                    list_item_nodes.append(ParentNode("li", children))
                # else: handle malformed line? For now, assume block_to_block_type was correct
            block_nodes.append(ParentNode("ol", list_item_nodes))

        # else: Should not happen if block_to_block_type is exhaustive

    # Wrap all block nodes in a single root div
    root_node = ParentNode("div", block_nodes)
    return root_node