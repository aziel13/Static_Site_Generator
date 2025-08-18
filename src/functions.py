
from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            lnode = LeafNode(None, text_node.text)
        case TextType.Bold:
            lnode = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            lnode = LeafNode("i", text_node.text)
        case TextType.CODE:
            lnode = LeafNode("code", text_node.text)
        case TextType.LINK:
            lnode = LeafNode("a", text_node.text)
        case TextType.IMAGE:
            lnode = LeafNode("img", text_node.text)
        case __:
            raise Exception("Unknown text type")

    return lnode

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []


    for old_node in old_nodes:

        text = old_node.text
        oldtype = old_node.text_type

        split_node = text.split(delimiter)
        new_node = []
        if len(split_node) > 1:
            delimited_text = ""
            for i in range(0, len(split_node)):
                if i == 0:
                    new_nodes.append(TextNode(split_node[i], oldtype))
                elif i > 0 and i < len(split_node) - 1:

                    delimited_text +=  split_node[i].replace("**", "")

                else:
                    new_nodes.append(TextNode(delimited_text, text_type))

                    new_nodes.append(TextNode(split_node[i], oldtype))

        else:
            new_nodes.append(TextNode(text, oldtype))

    return new_nodes