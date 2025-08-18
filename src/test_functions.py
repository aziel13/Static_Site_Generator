import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from functions import text_node_to_html_node, split_nodes_delimiter


class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):


        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)

        result = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
                ]

        self.assertEqual(split_nodes_delimiter([node],"**", TextType.BOLD), result)


    def test_split_nodes_nested_delimiter(self):


        node = TextNode("This is a **nested **bold** word**.", TextType.TEXT)

        result = [
                TextNode("This is a ", TextType.TEXT),
                TextNode("nested bold word", TextType.BOLD),
                TextNode(".", TextType.TEXT),
                ]

        self.assertEqual(split_nodes_delimiter([node],"**", TextType.BOLD), result)

    def test_split_nodes_no_delimiter_in_text(self):
        node = TextNode("This is just text.", TextType.TEXT)

        result = [
            TextNode("This is just text.", TextType.TEXT)
        ]

        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), result)

    def test_split_nodes_nested_diff_delimiter(self):
        node = TextNode("This is an _italic and **bold** word_.", TextType.TEXT)

        result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("_italic and ", TextType.ITALIC),
            TextNode("**bold**", TextType.BOLD),
            TextNode(" word_", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]

        self.assertNotEqual(split_nodes_delimiter([node], "**", TextType.BOLD), result)