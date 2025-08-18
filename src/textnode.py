from enum import Enum

class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url = None ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_text_node):

        same_text = self.text == other_text_node.text
        same_text_type = self.text_type == other_text_node.text_type
        same_url = self.url == other_text_node.url

        return  same_text and same_text_type and same_url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
