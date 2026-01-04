import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as file:
        mdx = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_content = markdown_to_html_node(mdx).to_html()
    title = extract_title(mdx)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("no title found")
