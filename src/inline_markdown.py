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

def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        for image_alt, image_link in images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            original_text = sections[1] if len(sections) > 1 else ""

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_links(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        for link_text, link_src in links:
            sections = original_text.split(f"[{link_text}]({link_src})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_src))

            original_text = sections[1] if len(sections) > 1 else ""

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
