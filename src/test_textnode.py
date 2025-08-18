import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):

        text = "This is a text node"
        text_type = TextType.BOLD

        node = TextNode(text, text_type)
        node2 = TextNode(text, text_type)

        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()