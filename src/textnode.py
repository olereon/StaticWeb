from enum import Enum

class TextType(Enum):
    TEXT = "text"           # Normal text
    BOLD = "bold"           # **Bold text**
    ITALIC = "italic"       # _Italic text_
    CODE = "code"           # `Code text`
    LINK = "link"           # [anchor text](url)
    IMAGE = "image"         # ![alt text](url)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
# ... (Keep HTMLNode, LeafNode, ParentNode, text_node_to_html_node as they are) ...

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"