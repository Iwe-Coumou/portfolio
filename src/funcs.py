from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode
from blocks import BlockType
from parentnode import ParentNode
import re
import os
import shutil

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Text type not supported")
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"There was a delimiter that was not closed")
        
        nodes = []
        is_text = True
        for text in split_text:
            if text == "":
                is_text = not is_text
                continue
            if is_text:
              nodes.append(TextNode(text=text, text_type=TextType.TEXT))  
            else:
                nodes.append(TextNode(text=text, text_type=text_type))
            is_text = not is_text
        new_nodes.extend(nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        nodes = []
        to_be_processed = None
        for match in matches:
            text_to_split = to_be_processed if to_be_processed is not None else node.text
            split = text_to_split.split(f"![{match[0]}]({match[1]})", 1)
            if split[0] != "":
                nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
            nodes.append(TextNode(text=match[0], text_type=TextType.IMAGE, url=match[1]))
            if split[1] == "":
                break
            if match == matches[-1]:
                nodes.append(TextNode(text=split[1], text_type=TextType.TEXT))
            else:
                to_be_processed = split[1]
        new_nodes.extend(nodes)
    return new_nodes
            
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        
        nodes = []
        to_be_processed = None
        for match in matches:
            text_to_split = to_be_processed if to_be_processed is not None else node.text
            split = text_to_split.split(f"[{match[0]}]({match[1]})", 1)
            if split[0] != "":
                nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
            nodes.append(TextNode(text=match[0], text_type=TextType.LINK, url=match[1]))
            if split[1] == "":
                break
            if match == matches[-1]:
                nodes.append(TextNode(text=split[1], text_type=TextType.TEXT))
            else:
                to_be_processed = split[1]
        new_nodes.extend(nodes)
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, delimiter="`", text_type=TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block != ""]

def block_to_blocktype(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    if re.match(r'^```\n[\s\S]+```$', block):
        return BlockType.CODE
    if all([line.startswith(">") for line in block.split("\n")]):
        return BlockType.QUOTE
    if all([line.startswith("- ") for line in block.split("\n")]):
        return BlockType.U_List
    if all(line.startswith(f"{i}. ") for i, line in enumerate(block.split("\n"), 1)):
        return BlockType.O_LIST
    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text=text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_node(block: str, block_type: BlockType) -> HTMLNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=text_to_children(block))
        case BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count+=1
                else:
                    break
            return ParentNode(tag=f"h{count}", children=text_to_children(block[count+1:]))
        case BlockType.CODE:
            return text_node_to_html_node(TextNode(text=block.split("\n", 1)[1].rsplit("\n", 1)[0], text_type=TextType.CODE))
        case BlockType.QUOTE:
            items = block.split("\n")
            filtered = [item[1:].strip() for item in items if item[1:].strip() != ""]
            children = text_to_children(" ".join(filtered))
            return ParentNode(tag='blockquote', children=children)
        case BlockType.U_List:
            items = block.split("\n")
            li_nodes = [ParentNode(tag="li", children=text_to_children(item[2:])) for item in items]
            return ParentNode(tag="ul", children=li_nodes)
        case BlockType.O_LIST:
            items = block.split("\n")
            li_nodes = [ParentNode(tag="li", children=text_to_children(item.split(". ", 1)[1])) for item in items]
            return ParentNode(tag='ol', children=li_nodes)
        case _:
            raise ValueError(f"Block type ({block_type}) not suported")

def markdown_to_html_node(markdown: str) -> ParentNode:
    if len(markdown) == 0:
        return None
    blocks = markdown_to_blocks(markdown=markdown)
    children = []
    for block in blocks:
        block_type = block_to_blocktype(block=block)
        block_node = block_to_node(block, block_type)
        children.append(block_node)
    return ParentNode(tag="div", children=children)
    
    
def copy_content(src: str, dest: str) -> None:
    src = os.path.abspath(src)
    dest = os.path.abspath(dest)
    
    
    if not os.path.exists(src):
        raise ValueError(f"Source ({src}) does not exist")
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted tree at {dest}")
    if not os.path.exists(dest):
        os.mkdir(dest)
        print(f"Created directory {dest}")
    
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        dest_path = os.path.join(dest, path)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied {src_path} -> {dest_path}")
        if os.path.isdir(src_path):
            copy_content(src_path, dest_path)

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_blocktype(block) == BlockType.HEADING and block.startswith("# "):
            return block.lstrip("#").strip()
    raise ValueError(f"No h1 title found")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
        
    node = markdown_to_html_node(content)
    # for i, child in enumerate(node.children):
    #     print(f"Child {i}: {child}")
    #     if hasattr(child, 'children') and child.children:
    #         for j, grandchild in enumerate(child.children):
    #             print(f"  Grandchild {i}.{j}: {grandchild}")
    html_str = node.to_html()
    title = extract_title(content)
    
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages(from_dir: str, template_path: str, dest_dir: str):
    if not os.path.exists(from_dir):
        print(f"Directory ({from_dir}) does not exist")
        return
        
    for item in os.listdir(from_dir):
        full_src = os.path.join(from_dir, item)
        full_dest = os.path.join(dest_dir, item)
        if os.path.isfile(full_src) and item.endswith(".md"):
            dest_name = item.replace(".md", ".html")
            generate_page(full_src, template_path, os.path.join(dest_dir, dest_name))
        if os.path.isdir(full_src):
            generate_pages(full_src, template_path, full_dest)