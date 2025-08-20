from textnode import TextNode
from textnode import TextType

from functions import copy_from_static_to_public

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)

    copy_from_static_to_public()

if __name__ == '__main__':
    main()
