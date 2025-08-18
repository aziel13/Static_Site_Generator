import unittest
import copy

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):

        node = LeafNode("p", "This is a paragraph of text.")

        node2 = copy.deepcopy(node)

        print(node.__eq__(node2))

        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()