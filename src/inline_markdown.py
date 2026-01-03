import re
from textnode import TextType, TextNode

def create_text_nodes(nodes, alt_type):
    new_nodes = []
    for i in range(len(nodes)):
        if i % 2 == 0:
            new_nodes.append(TextNode(nodes[i], TextType.TEXT))
        else:
            new_nodes.append(TextNode(nodes[i], alt_type))

    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown!")

        new_nodes.extend(create_text_nodes(parts, text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
