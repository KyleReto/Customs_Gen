from PIL import Image, ImageFont, ImageDraw
import json
import re
import copy
import unittest.mock as mock

# Development code
card = mock.Mock()
template_path = './templates/street_fighter/'
config_path = './config.json'
f = open(template_path + 'template_info.json')
template_info = json.load(f)
f.close()
f = open(config_path)
config_info = json.load(f)
f.close()
card.name = "PAPELNE"
card.card_type = "Character"
card.owner = 'Arc System Works'
card.copies = 1
card.text_box = """<italic></italic>Character text
<bold>Bold text:</bold> Normal Text <italic>(Italic Text)</italic>
This character can <bold>  -- Critical</bold> <italic>for <bold>2 Gauge, \nand will spin until he counters</bold></italic>
<bold><#FF0000>+2 Power</#FF0000></bold>
(\" --\" = crit symbol)\\<\\>/"""
card.cost = 3
card.secondary_cost = 2
card.secondary_type = 'Critical'
card.template_info = template_info
card.config_info = config_info
# End development code

# Open and closes tags as needed using lists to manage their states
def manage_tags(tag_str, color_list, style_list):
    if tag_str[0] == '/':
        if tag_str[1] == '#':
            color_list.pop()
        else:
            style_list.pop()
    else:
        if tag_str[0] == '#':
            color_list.append(tag_str)
        else:
            style_list.append(tag_str)

# Converts a string with bespoke markdown into a plaintext string and corresponding formatting information
def parse_markdown(str):
    # array of 3-tuples (style, color, text)
    string_data = []
    style = ['regular']
    color = ['#000000']
    # Matches any unescaped '<' or '>'
    for index, substr in enumerate(re.split(r'(?<!\\)[<>]', str)):
        # Odd outputs are always text, even is always formatting info
        if index % 2 == 0:
            final_style = style[-1]
            if (style.count('bold') and style.count('italic')):
                final_style = 'bold_italic'
            # Remove any escape characters left over
            string_data += [(final_style, color[-1], re.sub(r'(?<!\\)\\', '', substr))]
        else:
            manage_tags(substr, color, style)
            
    # Remove any left over empty string sections
    string_data = [element for element in string_data if element[2] != '']
    return string_data


# Composite two images, where the first is larger than the second.
# canvas = PIL image object
# addition_dict = dict with path and offsets defined
def composite_images(canvas, addition_dict):
    dest_offsets, src_offsets = [0,0], [0,0]
    try:
        dest_offsets = addition_dict['dest_offsets']
        src_offsets = addition_dict['source_offsets']
    except KeyError:
        print(f"Missings some offset definitions for \"{addition_dict['path']}\". "\
              "Using default offsets of 0 where definitions  are missing.")
    finally:
        try:
            with Image.open(addition_dict['path']) as addition_image:
                canvas.alpha_composite(addition_image, tuple(dest_offsets), tuple(src_offsets))
        except FileNotFoundError:
            print(f"Couldn't find a file at path \"{addition_dict['path']}.\" "\
            "If an image for this object exists in this template, "\
            "make sure that it's defined correctly in template_info.json.")
    return canvas

def draw_badges(image, substr, font, substr_offset, badge_dict):
    draw = ImageDraw.Draw(image)
    out_im = image
    for badge_key in badge_dict:
        for badge_match in (re.finditer(badge_key, substr)):
            draw_box = draw.textbbox((substr_offset,0), substr[0:badge_match.start()], font=font)
            new_dict = copy.deepcopy(badge_dict[badge_key])
            new_dict['dest_offsets'][0] = new_dict['dest_offsets'][0] + draw_box[2]
            print(new_dict)
            out_im = composite_images(out_im, new_dict)
    return out_im

# Converts a markdown object into an array of images, where each is a line of text.
# Badge dict is dict of {replace_str:badge_img_path}
def compose_text(markdown_objects, font_paths, font_size, badge_dict={}):
    # If only one font style is defined, add more.
    safe_font_paths = font_paths + [font_paths[0],font_paths[0],font_paths[0]]
    fonts = {'regular':ImageFont.truetype(safe_font_paths[0], font_size),
             'bold':ImageFont.truetype(safe_font_paths[1], font_size),
             'italic':ImageFont.truetype(safe_font_paths[2], font_size),
             'bold_italic':ImageFont.truetype(safe_font_paths[3], font_size)}
    txt_arr = [Image.new("RGBA", (5000,200),(0,0,0,0))]
    x_offset = 0
    for style, color, text_data in markdown_objects:
        substrings = text_data.split('\n')
        for idx, substr in enumerate(substrings):
            if (idx >= 1):
                txt_arr[-1].crop((0,0,x_offset,font_size))
                txt_arr += [Image.new("RGBA", (5000,200),(0,0,0,0))]
                x_offset = 0
            draw = ImageDraw.Draw(txt_arr[-1])
            draw_box = draw.textbbox((x_offset,0), substr, font=fonts[style])
            draw.text((x_offset,0), substr, color, font=fonts[style])
            txt_arr[-1] = draw_badges(txt_arr[-1], substr, fonts[style], x_offset, badge_dict)
            x_offset += draw_box[2]-draw_box[0]
    return txt_arr

def get_line_height(font_size, num_lines, box_height):
    used_space = font_size * num_lines
    num_breaks = num_lines - 1
    free_space = box_height - used_space
    try:
        line_size = free_space//num_breaks + font_size
    except ZeroDivisionError:
        line_size = free_space + font_size
    return line_size

def text_by_style(image, text, style_dict, badge_dict={}):
    return draw_text(image, text, style_dict['fonts'],style_dict['bounding_box'], 
                  max_font_size=style_dict['default_font_size'], max_vertical_spacing=style_dict['default_line_height'], badge_dict=badge_dict)

# Draws text in the canvas, converting between styles and adjusting size and spacing on the fly
# canvas = PIL Image object
# text = raw string data (to be passed to the markdown parser)
# font_files = (regular, bold, italic, bold-italic), all paths to their otf/ttf files
# bounding_box = (left, top, right, bottom), all in pixels from the top-left of the image
# max_font_size = largest font size to scale up to, in pixels.
# max_vertical_spacing = largest space between lines, in pixels.

# Draw at max font size, then scale down dynamically.
def draw_text(canvas, text, font_files, bounding_box, max_font_size=33, max_vertical_spacing=50, align='center', badge_dict={}):
    markdown_objects = parse_markdown(text)
    text_size = (bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1])
    image_lines = compose_text(markdown_objects, font_files, max_font_size, badge_dict=badge_dict)
    line_height = min(max_vertical_spacing, get_line_height(max_font_size, len(image_lines),text_size[1]))
    text_image = Image.new("RGBA", (5000,5000),(0,0,0,0))
    cursor_y = 0
    max_width = 0
    for idx, line in enumerate(image_lines):
        center_x = text_image.size[0] // 2
        line_bbox = line.getbbox()
        cursor_y = idx*line_height
        text_location = (center_x-line_bbox[2]//2,cursor_y)
        text_image.alpha_composite(line,text_location,(0,0))
        if line_bbox[2] > max_width:
            max_width = line_bbox[2]
    if max_width > text_size[0]:
        print('Text is too wide, shrinking...')
        resize_factor = text_size[0] / max_width
        old_dimensions = text_image.size
        new_dimensions = (int(old_dimensions[0]*resize_factor),int(old_dimensions[1]*resize_factor))
        text_image = text_image.resize(new_dimensions, resample=Image.LANCZOS)
    dest_corner = (bounding_box[0], bounding_box[1])
    source_corner = ((text_image.size[0]-text_size[0])// 2, 0)
    canvas.alpha_composite(text_image, dest_corner,source_corner)
    return canvas

def generate_character(card):
    template_images = card.template_info["images"]
    config_images = card.config_info["images"]
    text = card.template_info['text']

    with Image.new("RGBA", tuple(card.config_info['image_size_px']),(0,0,0,0)) as card_image:
        composite_images(card_image, template_images["character_background"])
        composite_images(card_image, config_images["character_image"])
        composite_images(card_image, template_images["character_frame"])
        composite_images(card_image, template_images["character_critical"])
        composite_images(card_image, template_images["exceed_flip"])
        text_by_style(card_image, str(card.cost), text['stats'])
        text_by_style(card_image, card.text_box, text['card_effect'], badge_dict=template_info["badges"])
        text_by_style(card_image, card.name, text['card_name'])
        text_by_style(card_image, f"<bold>FAN CARD NOT OFFICIAL. Exceed © Level 99 Games. {card.name} © {card.owner}. All assets copyright their respective owners.</bold>", text['watermark'])
        return card_image

generate_character(card).save('output/character.png')