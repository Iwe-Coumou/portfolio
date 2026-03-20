from funcs import copy_content
import os

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    copy_content(os.path.join(root, "static"), os.path.join(root, "public"))

if __name__ == "__main__":
    main()