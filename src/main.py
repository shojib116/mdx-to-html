import os
import shutil
from copystatic import copy_files_recursive


def main():
    copyTo = "./public"
    copyFrom = "./static"

    if os.path.exists(copyTo):
        shutil.rmtree(copyTo)
    os.mkdir(copyTo)

    if not os.path.exists(copyFrom):
        raise Exception("static directory could not be found")
    
    print("Copying static files to public directory")
    copy_files_recursive(copyFrom, copyTo)

main()

