
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):

        if value is None:
            raise ValueError("value cannot be None")

        super().__init__(tag, value, None, props)

    def to_html(self):
        html = f"";

        match self.tag:
            case "h1": html = f"<h1>{self.value}</h1>"
            case "h2": html = f"<h2>{self.value}</h2>"
            case "h3": html = f"<h2>{self.value}</h3>"
            case "h4": html = f"<h4>{self.value}</h4>"
            case "h5": html = f"<h5>{self.value}</h5>"
            case "h6": html = f"<h6>{self.value}</h6>"
            case "a": html = f"<a href=\"{self.props["href"]}\">{self.value}</a>"
            case "p": html = f"<p>{self.value}</p>"
            case "img": html = f"<img src=\"{self.props["image"]['src']}\">"
            case "b": html = f"<b>{self.value}</b>"
            case "li": html = f"<li>{self.value}</li>"
            case "ul": html = f"<ul>{self.value}</ul>"
            case "ol": html = f"<ol>{self.value}</ol>"
            case "span": html = f"<span>{self.value}</span>"
            case "div": html = f"<div>{self.value}</div>"
            case "em": html = f"<em>{self.value}</em>"
            case "i": html = f"<i>{self.value}</i>"
            case None: html = self.value
            case _: pass

        return html
