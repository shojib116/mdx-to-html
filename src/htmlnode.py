class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        attr = ""

        if self.props == None:
            return attr 

        attrLst = []
        for prop, val in self.props.items():
            attrLst.append(f"{prop}='{val}'")
        
        attr = (" ").join(attrLst)

        return attr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError

        if self.tag == None:
            return self.value

        if self.props_to_html() != "": 
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")

        if self.children == None:
            raise ValueError("Parent nodes must have a children")

        children = ""
        for child in self.children:
            children += child.to_html()

        if self.props_to_html() != "": 
            return f"<{self.tag} {self.props_to_html()}>{children}</{self.tag}>"

        return f"<{self.tag}>{children}</{self.tag}>"
