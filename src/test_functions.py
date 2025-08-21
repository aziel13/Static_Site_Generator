import unittest

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from functions import *
from blocks import BlockType


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
                TextNode("nested ", TextType.BOLD),
                TextNode("bold", TextType.TEXT),
                TextNode(" word", TextType.BOLD),
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


    def test_split_nodes_two_same_delimiter(self):
        node = TextNode( "An elaborate pantheon of deities (the `Valar` and `Maiar`)", TextType.TEXT)

        ExpectedResult = [
            TextNode("An elaborate pantheon of deities (the ", TextType.TEXT),
            TextNode("Valar", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("Maiar", TextType.CODE),
            TextNode(")", TextType.TEXT)
        ]

        ActualResult = split_nodes_delimiter([node], "`", TextType.CODE)

        print("ActualResult",ActualResult)

        self.assertEqual(ActualResult, ExpectedResult)

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
                TextNode(" and a ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
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

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_paragraph(self):
        markdown = "nothing special about this paragraph \n yes \n indeed"

        expected_output = BlockType.PARAGRAPH
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)


    def test_markdown_heading(self):
        markdown = "##### heading text"

        expected_output = BlockType.HEADING1
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)


    def test_markdown_code_block(self):
        markdown = "``` print(\"Hello World\") ```"

        expected_output = BlockType.CODE
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)


    def test_markdown_qoute_block(self):
        markdown = ">Wisdom comes from experience.\n>Experience is often a result of lack of wisdom.\n>Terry Pratchett"

        expected_output = BlockType.QUOTE
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)


    def test_markdown_unordered_list(self):
        markdown = "- milk\n- cheese\n- Mushrooms"

        expected_output = BlockType.UNORDEREDLIST
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)

    def test_markdown_ordered_list(self):
        markdown = "1. ichi\n2. ni\n3. san"

        expected_output = BlockType.ORDEREDLIST
        actual_output = block_to_block_type(markdown)
        self.assertEqual(expected_output, actual_output)

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        html_expected = "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"

        self.assertEqual(
            html,
            html_expected,
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        html_expected = "<div><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></div>"


        print()
        print()
        print(f"html: {html}")
        print()
        print()
        print(f"html: {html_expected}")


        self.assertEqual(
            html,
            html_expected,
        )

    def test_extract_title(self):
        md = """
            # title
            This is text that _should_ remain
            the **same** even with inline stuff
            """

        expected_title = "<h1>title</h1>"
        actual_title = extract_title(md)

        self.assertEqual(
            expected_title,
            actual_title,
        )


    def test_extract_no_title(self):
        md = """
            This is text that _should_ remain
            the **same** even with inline stuff
            """
        expected_exception = "No title found"

        try:
            actual_title = extract_title(md)
        except Exception:
            self.assertRaises( Exception, expected_exception)


    def test_extract_no_h1_title(self):
        md = """
            ## title
            This is text that _should_ remain
            the **same** even with inline stuff
            """

        expected_exception = "No title found"
        try:
            actual_title = extract_title(md)
        except Exception:
            self.assertRaises(Exception, expected_exception)

