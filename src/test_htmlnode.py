import unittest
import copy

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):

        node = HTMLNode()
        node2 = copy.deepcopy(node)

        print(node.__eq__(node2))

        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()