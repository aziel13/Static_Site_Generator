import os
import shutil
from site import abs_paths

from click import clear
from rich import markdown

from textnode import TextNode, TextType
from leafnode import LeafNode

import re
from parentnode import ParentNode
from htmlnode import HTMLNode

from blocks import BlockType

def text_nodes_to_html_nodes(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            lnode = LeafNode(None, text_node.text)
        case TextType.BOLD:
            lnode = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            lnode = LeafNode("i", text_node.text)
        case TextType.CODE:
            lnode = LeafNode("code", text_node.text)
        case TextType.LINK:
            lnode = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            lnode = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case __:
            raise Exception("Unknown text type")

    return lnode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):

    new_nodes = []

    for old_node in old_nodes:

        text = old_node.text
        new_text = text
        image_pattern = r"[!]\[.+?\]\(.+?\)"

        #inject delimiter to split on that seperates images from regular text

        matches = re.finditer(image_pattern, text)

        if re.search(image_pattern, text) is not None:

            match_indexies = []


            for match in matches:
                #print(match.group())
                match_index = (match.start(), match.end())
                match_indexies.append(match_index)

            index_offset = 0

            for match_index in match_indexies:

                new_text = f"{new_text[0:match_index[0]+index_offset]}*^*{new_text[match_index[0]+index_offset:match_index[1]+index_offset]}*^*{new_text[match_index[1]+index_offset:len(new_text)]}"
                index_offset += 6
           # print(f"new_text = {new_text}")
            split_text = new_text.split("*^*")

            for str in split_text:
               # print(f"match = {str}")

                if re.match(image_pattern,str) is not None:

                    tup_list = extract_markdown_images(str)

                    for tup in tup_list:
                        new_nodes.append(TextNode(tup[0], TextType.IMAGE, tup[1]))

                elif str.strip() != "":

                    new_nodes.append(TextNode(str, TextType.TEXT))
        else:
            new_nodes.append(old_node)
        #for node in new_nodes:
        #    print(node)

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []

    for old_node in old_nodes:

        text = f" {old_node.text}"

        new_text = text

        link_pattern = r"[^!]\[.+?\]\(.+?\)"

        matches = re.finditer(link_pattern, text)

        if re.search(link_pattern, text) is not None:

            match_indexies = []


            for match in matches:
                #print(match.group())
                match_index = (match.start(), match.end())
                match_indexies.append(match_index)

            index_offset = 0

            for match_index in match_indexies:

                new_text = f"{new_text[0:match_index[0]+index_offset]} *^*{new_text[match_index[0]+index_offset:match_index[1]+index_offset]} *^*{new_text[match_index[1]+index_offset:len(new_text)]}"
                index_offset += 8
            #print(new_text)

            #inject delimiter to split on that seperates images from regular text
            #new_text = text.replace(pattern, "*^*^*[").replace(pattern2, ")*^*^*")

            #print(f"new_text = {new_text}")

            split_text = new_text[1:-1].split("*^*")

            for str in split_text:

               # print(f"match = {str}")
                if re.match(link_pattern,str) is not None:

                    tup_list = extract_markdown_links(str)

                    for tup in tup_list:
                        new_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))

                elif str.strip() != "":

                    new_nodes.append(TextNode(str, TextType.TEXT))

           # for node in new_nodes:
             #   print(f"node: {node}")
        else:
            new_nodes.append(old_node)

    return new_nodes

def extract_markdown_images(text):
    tuplist = []

    image_pattern = r"[!]\[.+?\]\(.+?\)"

    markdown_image_matches = re.findall(image_pattern,text)

    for match in markdown_image_matches:

     #   alt_text = re.findall(alttext_r,match)

        if "![" in match and "]" in match:
            new_match_text = match.replace("![", "").replace("]", "*^*").replace("(", "").replace(")", "")
            split_text = new_match_text.split("*^*")

            tuplist.append((split_text[0], split_text[1]))

    #print(f"tuplist: {tuplist}")

    return tuplist

def extract_markdown_links(text):
    tuplist = []

    link_pattern = r"[^!]\[.+?\]\(.+?\)"

    link_matches = re.findall(link_pattern, text)

    #print(f"alt_text_url_matches = {alt_text_url_matches}")

    for match in link_matches:
       # text = re.findall(text_r, match)
       # url = re.findall(url_r, match)

        if "![" not in match and "[" in match and "]" in match:

            new_match_text = match.replace(" [", "").replace("[", "").replace("]", "*^*").replace("(", "").replace(")", "")

            split_text = new_match_text.split("*^*")

            tuplist.append((split_text[0], split_text[1]))

    return tuplist


def text_to_textnodes(text):



    new_nodes = [TextNode(text, TextType.TEXT)]


    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)

    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    new_nodes = split_nodes_image(new_nodes)

    new_nodes = split_nodes_link(new_nodes)

    # print("[")
    # for node in new_nodes:
    #     print(f"{node}")
    # print("]")

    return new_nodes

def markdown_to_blocks(markdown):

    split_list = markdown.split("\n\n")

    blocks = []
    #print("[")
    for i in range(0, len(split_list)):

        block = split_list[i].strip()

        splitblocks = block.split("\n")
        stripedblocks = []

        for block in splitblocks:
            stripedblocks.append(block.strip())

        block = "\n".join(stripedblocks)

        if block != "":
            blocks.append(block)

    #for block in blocks:
     #   print(block)


    return blocks

def block_to_block_type (markdown):

    block_type = None

    split_list = markdown.split("\n")

    is_qoute = True

    is_unordered = True

    is_ordered = True

    #print(len(split_list))

    if len(markdown) > 0:

        beginning = markdown[0:3]
        ending = markdown[len(markdown)-3:len(markdown)]

        if markdown[0] == "#" or markdown[0:1] == "##" or markdown[0:2] == "###"or markdown[0:3] == "####"or markdown[0:4] == "#####"or markdown[0:5] == "######":
            if markdown[0] == "#":
                block_type = BlockType.HEADING1
            elif markdown[0:1] == "##":
                block_type = BlockType.HEADING2
            elif markdown[0:2] == "###":
                block_type = BlockType.HEADING3
            elif markdown[0:3] == "####":
                block_type = BlockType.HEADING4
            elif markdown[0:4] == "#####":
                block_type = BlockType.HEADING5
            elif markdown[0:5] == "######":
                block_type = BlockType.HEADING6


        elif beginning == "```" and ending == "```":
            block_type = BlockType.CODE

        elif markdown.startswith(">"):
            block_type = BlockType.QUOTE

            for line in split_list:
                if not line.startswith(f">"):
                    return BlockType.PARAGRAPH

        elif markdown.startswith("- "):
            block_type = BlockType.UNORDEREDLIST

            for line in split_list:
                if not line.startswith(f"- "):
                    return BlockType.PARAGRAPH

        elif markdown.startswith("1. "):
            i = 1
            for line in split_list:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
                i += 1

            block_type = BlockType.ORDEREDLIST

        else:
            block_type = BlockType.PARAGRAPH



    return block_type


def text_to_children(text):

    htmlchildnodes = text_nodes_to_html_nodes(text_to_textnodes(text))

    # for node in htmlchildnodes:
    #     print(node.to_html())


    return htmlchildnodes

def text_block_to_html_parent_node(text_block):


    text_block_type = block_to_block_type(text_block)

    if text_block_type == BlockType.CODE:

        text_block = text_block.replace("```\n", "").replace("```", "")



        child_nodes = text_nodes_to_html_nodes([TextNode(text_block, TextType.TEXT)])
    elif text_block_type == BlockType.ORDEREDLIST:

        child_nodes = []

        lines = text_block.split("\n")
        i = 1

        for line in lines:
            pattern = f"{i}. "
            line = re.sub(pattern, "", line)

            child = text_to_children(line)
            pnode = ParentNode("li",child)
            child_nodes.append(pnode)

            i += 1

    elif text_block_type == BlockType.UNORDEREDLIST:

        child_nodes = []

        lines = text_block.split("\n")

        i = 1

        for line in lines:
            pattern = f"- "
            line = re.sub(pattern, "", line)
            child = text_to_children(line)
            pnode = ParentNode("li",child)
            child_nodes.append(pnode)

            i += 1
    elif text_block_type == BlockType.QUOTE:
        child_nodes = []


        pattern = f">"
        line = re.sub(pattern, "", text_block).strip()
        child_nodes = text_to_children(line)


    else:
        child_nodes = text_to_children(text_block)

    match text_block_type:
        case BlockType.HEADING1:
            parent_node = ParentNode("h1", child_nodes)
        case BlockType.HEADING2:
            parent_node = ParentNode("h2", child_nodes)
        case BlockType.HEADING3:
            parent_node = ParentNode("h3", child_nodes)
        case BlockType.HEADING4:
            parent_node = ParentNode("h4", child_nodes)
        case BlockType.HEADING5:
            parent_node = ParentNode("h5", child_nodes)
        case BlockType.HEADING6:
            parent_node = ParentNode("h6", child_nodes)
        case BlockType.CODE:
            parent_node = ParentNode("code", child_nodes)
        case BlockType.QUOTE:
            parent_node = ParentNode("blockquote", child_nodes)
        case BlockType.UNORDEREDLIST:
            parent_node = ParentNode("ul", child_nodes)
        case BlockType.ORDEREDLIST:
            parent_node = ParentNode("ol", child_nodes)
        case _:
            parent_node = ParentNode("p", child_nodes)

    return parent_node

def markdown_to_html_node(markdown):

    text_nodes = []

    markdown_blocks = markdown_to_blocks(markdown)

    html_parent_nodes = []

    for block in markdown_blocks:

        if len(block) > 0:
            parent_node = text_block_to_html_parent_node(block)
            html_parent_nodes.append(parent_node)

    html_parent_node = ParentNode("div", html_parent_nodes)

    return html_parent_node

def copy_from_static_to_public(working_directory= ".", source_directory="static", dest_directory="public"):

    abs_working_dir = os.path.abspath(working_directory)
    abs_source_dir = os.path.abspath(os.path.join(working_directory, source_directory))
    abs_dest_dir = os.path.abspath(os.path.join(working_directory, dest_directory))

    if not abs_source_dir.startswith(abs_working_dir):
        raise Exception(f'Error: Cannot list "{source_directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_source_dir):
        raise Exception(f'Error: "{source_directory}" is not a directory')

    if not abs_source_dir.startswith(abs_working_dir):
        raise Exception(f'Error: Cannot list "{abs_dest_dir}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_dest_dir):
        raise Exception(f'Error: "{abs_dest_dir}" is not a directory')

    # delete from directory
    for filename in os.listdir(abs_dest_dir):
        file_path = os.path.join(abs_dest_dir, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

        if os.path.isdir(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

    # copy files from source directory to dest directory

    # Iterate over all items in the source directory
    for item in os.listdir(abs_source_dir):
        source_path = os.path.join(abs_source_dir, item)
        destination_path = os.path.join(abs_dest_dir, item)

        # Check if the item is a file before copying
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Copied '{item}' to '{dest_directory}'")
        else:

            new_source_directory = f"{source_directory}/{item}"
            new_destination_directory = f"{dest_directory}/{item}"

            os.makedirs(new_destination_directory, exist_ok=True)

            print(f"copying '{item}' as its a directory, not a file)")
            copy_from_static_to_public(working_directory=".", source_directory=new_source_directory, dest_directory=new_destination_directory)

def extract_title(markdown):

    if "#" in markdown:

        markdown_split = markdown.split("\n")

        for text in markdown_split:
            if "#" in text and text.count("#") == 1:
                return f"<h1>{text.replace("#","").strip()}</h1>"

    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page: {from_path} to {dest_path} using {template_path}")

    markdown = None
    template = None

    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
        markdown_file.close()

    with open(template_path, "r") as template_file:
        template = template_file.read()
        template_file.close()

    html = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    #print(html)
    #print(title)
    pattern = "{{ Title }}"
    pattern1 = "{{ Content }}"

    template = re.sub(pattern,title, template)
    template = re.sub(pattern1, html, template)
    #template.replace('{{ Title }}', f"<title>{title}</title>")
    #template.replace("{{ Content }}", html)

    #print(template)

    with open(dest_path, "w") as output_file:
        output_file.write(template)
        output_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        dir_path = os.path.join(dest_dir_path, filename)
        if file_path.endswith(".md") and os.path.isfile(file_path):

            new_dir_path = dir_path.replace(".md", ".html")

            generate_page(file_path, template_path, new_dir_path)

        elif os.path.isdir(file_path):

            new_dest_dir_path =  os.path.join(dest_dir_path, filename)

            os.makedirs(new_dest_dir_path, exist_ok=True)

            generate_pages_recursive(file_path, template_path, new_dest_dir_path)