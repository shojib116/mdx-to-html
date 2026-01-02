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




