import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]

def block_to_block_type(block):
    # Match heading
    if re.match(r"^#{1,6}\s.*$", block):
        return BlockType.HEADING

    # Match code block
    if re.match(r"^```(?!`)[\s\S]*?(?<!`)```$", block):
        return BlockType.CODE

    # Match quote block
    if block.startswith(">"):
        return BlockType.QUOTE

    # Match unordered list
    if re.match(r"^- .*(\n- .*)*$", block):
        return BlockType.UNORDERED_LIST

    # Match ordered list
    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

ordered_block_pattern = re.compile(r"^(\d+)\. .*(?:\n\d+\. .*)*$")

def is_ordered_list_block(text: str) -> bool:
    # must look like only ordered-list lines
    if not re.fullmatch(ordered_block_pattern, text):
        return False

    lines = text.split("\n")
    nums = []
    for line in lines:
        m = re.match(r"^(\d+)\. ", line)
        if not m:
            return False
        nums.append(int(m.group(1)))

    # now enforce 1,2,3,...
    if not nums:
        return False
    return nums[0] == 1 and nums == list(range(1, len(nums) + 1))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for c in block:
        if c == "#":
            level += 1
        else:
            break

    if level + 1 >= len(block):
        raise ValueError("Invalid heading level")

    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line[2:].strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
