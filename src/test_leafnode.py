import unittest
import copy

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):

        node = LeafNode("p", "This is a paragraph of text.")

        node2 = copy.deepcopy(node)

        print(node.__eq__(node2))

        self.assertEqual(node, node2)

    def test_output(self):

        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
if __name__ == "__main__":
    unittest.main()