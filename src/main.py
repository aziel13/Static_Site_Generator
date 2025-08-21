from textnode import TextNode
from textnode import TextType
import sys

from functions import copy_from_static_to_docs,generate_pages_recursive

def main():

    basepath = sys.argv[0]

    copy_from_static_to_docs()

    generate_pages_recursive(basepath,"content", "template.html", "docs")



if __name__ == '__main__':
    main()
