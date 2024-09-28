from htmlnode import HTMLNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown: str) -> list:

    lines = markdown.split('\n\n')
    blocks = [line.strip() for line in lines if line]

    return blocks

def block_to_block_type(markdown: str) -> str:
    lines = markdown.split('\n')

    if markdown.startswith(("#", "##", "###", "####", "#####", "######")):
        return block_type_heading
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
        
    if markdown.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
        
    
    if markdown.startswith("1. "):
        i = 1
        for line in lines: 
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        child_list = []

        if block_type == block_type_paragraph:
            html = HTMLNode(tag="p", value=block, children=None, props=None)
            print(block_type)
            child_list.append(html)

        # how to make sure num of # gets translated to html
        if block_type == block_type_heading:
            split_heading = block.split(" ")
            size = len(split_heading[0])
            htmlp = HTMLNode(tag=f"h{size}", value=" ".join(split_heading[1:]))
            child_list.append(htmlp)

            print(htmlp)

        # paragraph is easy
        # lists (both OL and UL) will need children

    return HTMLNode(tag="div", value=None, children=child_list, props=None)

    