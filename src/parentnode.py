
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):

        if tag is None:
            raise ValueError("tag cannot be None")

        if children is None:
            raise ValueError("children cannot be None")

        super().__init__(tag, None, children, props)

    def to_html(self):
        match self.tag:
            case "h1":
                head = "<h1>"
                tail = "</h1>"

            case "h2":
                head = "<h2>"
                tail = "</h2>"

            case "h3":
                head = "<h3>"
                tail = "</h3>"
            case "h4":
                head = "<h4>"
                tail = "</h4>"
            case "h5":
                head = "<h5>"
                tail = "</h5>"
            case "h6":
                head = "<h6>"
                tail = "</h6>"
            case "a":
                head = "<a>"
                tail = "</a>"
            case "p":
                head = "<p>"
                tail = "</p>"
            case "b":
                head = "<b>"
                tail = "</b>"
            case "li":
                head = "<li>"
                tail = "</li>"
            case "ul":
                head = "<ul>"
                tail = "</ul>"
            case "ol":
                head = "<ol>"
                tail = "</ol>"
            case "span":
                head = "<span>"
                tail = "</span>"
            case "div":
                head = "<div>"
                tail = "</div>"
            case "em":
                head = "<em>"
                tail = "</em>"
            case "i":
                head = "<i>"
                tail = "</i>"
            case "strong":
                head = "<strong>"
                tail = "</strong>"
            case "header":
                head = "<header>"
                tail = "</header>"
            case "html":
                head = "<html>"
                tail = "</html>"
            case "blockquote":
                head = "<blockquote>"
                tail = "</blockquote>"
            case "code":
                head = "<code>"
                tail = "</code>"
            case "style":
                head = "<style>"
                tail = "</style>"
            case "head":
                head = "<head>"
                tail = "</head>"
            case "body":
                head = "<body>"
                tail = "</body>"
            case _: pass

        html = "";



        for child in self.children:
            html += child.to_html();

        html = f"{head}{html}{tail}"

        return html
