from funcs import copy_content, generate_pages
import os
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_content(os.path.join(root, "static"), os.path.join(root, "docs"))
    generate_pages(os.path.join(root, "content"), os.path.join(root, "templates"), os.path.join(root, "docs"), basepath)
    

if __name__ == "__main__":
    main()