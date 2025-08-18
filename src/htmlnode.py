
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):

        href = None
        target = "_blank"

        if "href" in self.props:
            href = self.props["href"]

        if "target" in self.props:
            target = self.props["target"]

        return f" href=\"{href}\" target=\"{target}\""

    def __eq__(self, other_node):
        same_tag = self.tag == other_node.tag
        same_value = self.value == other_node.value
        same_children = self.children == other_node.children
        same_props = self.props == other_node.props

        return same_tag and same_value and same_children and same_props


    def __repr__(self):
        return f"tag:{self.tag} value:{self.value} children:{self.children} props:{self.props}"