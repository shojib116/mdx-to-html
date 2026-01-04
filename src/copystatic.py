import os
import shutil

def copy_files_recursive(copyFrom, copyTo):
    items = os.listdir(copyFrom)
    for item in items:
        item_path = os.path.join(copyFrom, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, copyTo)
            print("copied", item_path, "to", copyTo)
        else:
            dst = os.path.join(copyTo, item)
            os.mkdir(dst)
            copy_files_recursive(item_path, dst)
 
