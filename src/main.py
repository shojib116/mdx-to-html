import os
import sys
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)

    if not os.path.exists(dir_path_static):
        raise Exception("static directory could not be found")
    
    print("Copying static files to public directory")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
    )

main()

