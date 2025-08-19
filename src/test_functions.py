import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from functions import *


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )


        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches2 = extract_markdown_links(
            "This is text with an [image](https://Ex_nihilo/nihil_fit)"
        )


        self.assertListEqual([("image", "https://Ex_nihilo/nihil_fit")], matches2)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )



    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_image_w_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and a [link](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a [link](https://i.imgur.com/zjjcJKZ.png) ", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_link_w_image(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and a ![image](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and a ![image](https://i.imgur.com/zjjcJKZ.png) ", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        expected_output = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]

        actual_output = text_to_textnodes(text)

        self.assertListEqual(expected_output, actual_output)

        def test_text_to_text_nodes(self):
            text = "This is text with an _**italic**_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

            expected_output = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]

            actual_output = text_to_textnodes(text)

            self.assertNotEqual(expected_output, actual_output)
