import os
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, os.path.join(dest_dir_path, "index.html"), basepath)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(item_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as file:
        mdx = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_content = markdown_to_html_node(mdx).to_html()
    title = extract_title(mdx)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace("href='/", f"href='{basepath}")
    template = template.replace('src="/', f'src="{basepath}')
    template = template.replace("src='/", f"src='{basepath}")

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
