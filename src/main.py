from funcs import copy_content, generate_pages
import os

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_content(os.path.join(root, "static"), os.path.join(root, "public"))
    generate_pages("content", "template.html", "public")
    

if __name__ == "__main__":
    main()