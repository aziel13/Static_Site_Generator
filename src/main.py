from textnode import TextNode
from textnode import TextType

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)

if __name__ == '__main__':
    main()
