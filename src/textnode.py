from enum import Enum

class TextType(Enum):
    plain_text = "text (plain)"
    bold_text = "**Bold text**"
    italic_text = "_Italic text_"
    code_text = "`Code text`"
    link = "[anchor text](url)"
    image = "![alt text](url)"

class TextNode:
    def __init__(self, text, text_type, url = None ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eg__(self, text_node1, text_node2):

        return text_node1.text == text_node2.text and text_node1.text_type == text_node1.text_type and text_node1.url == text_node2.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"