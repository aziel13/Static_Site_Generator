from click import clear

from textnode import TextNode, TextType
from leafnode import LeafNode

import re

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            lnode = LeafNode(None, text_node.text)
        case TextType.Bold:
            lnode = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            lnode = LeafNode("i", text_node.text)
        case TextType.CODE:
            lnode = LeafNode("code", text_node.text)
        case TextType.LINK:
            lnode = LeafNode("a", text_node.text)
        case TextType.IMAGE:
            lnode = LeafNode("img", text_node.text)
        case __:
            raise Exception("Unknown text type")

    return lnode

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []


    for old_node in old_nodes:

        text = old_node.text
        oldtype = old_node.text_type

        split_node = text.split(delimiter)
        new_node = []

        if delimiter in old_node.text and len(split_node) > 1:

            delimited_text = ""
            for i in range(0, len(split_node)):
                if i == 0:
                    new_nodes.append(TextNode(split_node[i], oldtype))
                elif i > 0 and i < len(split_node) - 1:

                    delimited_text +=  split_node[i].replace(delimiter, "")

                else:
                    new_nodes.append(TextNode(delimited_text, text_type))

                    new_nodes.append(TextNode(split_node[i], oldtype))

        else:
            new_nodes.append(old_node)

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

        text = old_node.text

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

           # print(f"new_text = {new_text}")

            split_text = new_text.split("*^*")

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

    print("[")
    for node in new_nodes:
        print(f"{node}")
    print("]")

    return new_nodes
