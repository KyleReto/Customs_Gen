from PIL import Image, ImageFont, ImageDraw
import json
import re
import copy
import unittest.mock as mock
import csv

#select bold 
bold_words = ['Now:', 'Before:', 'Hit:', 'After:', 'Cleanup:', 'Ignore Armor', 'Ignore Guard', 'Critical', 'Strike', 'Advantage']
stat_words = {
    'Range': '#00abea',
    'Power': '#f54137',
    'Speed': '#fff5a5',
    'Armor': '#ae96c3',
    'Guard': '#39ab55'
}



# Development code
template_path = './templates/street_fighter/'
config_path = './config.json'
f = open(template_path + 'template_info.json', encoding='utf-8')
template_info = json.load(f)
f.close()
f = open(config_path, encoding='utf-8')
config_info = json.load(f)
f.close()

card = {}
card['card_name'] = "ULTRA NAME"
card['card_type'] = "Ultra"
card['owner'] = 'Character Name'
card['copies'] = 1
card['text_box'] = """Exceed Text
<bold>Bold text:</bold>  -- Normal Text <italic>(Italic Text)</italic>
<bold><@2#000000><#00abea>+0~1 Range</#></@>, <@2#000000><#00abea>+2-3 Range</#></@>, <@2#000000><#f54137>+1 Power</#></@>,
 <@2#000000><#fff5a5>-1 Speed</#></@>, <@2#000000><#ae96c3>+2 Armor</#></@>, <@2#000000><#39ab55>-4 Guard</#></@></bold>"""
card['secondary_text_box'] = '''Boost 1 Text
<bold>Bold text:</bold> Normal Text <italic>(Italic Text)</italic>
This boost costs 1 Force.'''
card['cost'] = '1'
card['secondary_cost'] = '1'
card['secondary_type'] = 'Force Boost'
card['secondary_subtype'] = 'Instant'
card['range'] = '4-5'
card['power'] = '3'
card['speed'] = '4'
card['armor'] = '5'
card['guard'] = '6'
card['secondary_name'] = 'ANGER CHARGE'
card['template_info'] = template_info
card['config_info'] = config_info
# End development code

default_img = {"path":"assets/default_image.png",
        "dest_offsets":[0,0],
        "source_offsets":[0,0]}
default_text = {
        "fonts":["assets/Minion Pro Regular.ttf"],
        "bounding_box":[0,0]+card['config_info']['image_size_px']
    }

# Open and closes tags as needed using lists to manage their states
def manage_tags(tag_str, color_list, style_list, outline_list):
    if tag_str[0] == '/':
        if tag_str[1] == '#':
            color_list.pop()
        elif tag_str[1] == '@':
            outline_list.pop()
        else:
            style_list.pop()
    else:
        if tag_str[0] == '#':
            color_list.append(tag_str)
        elif tag_str[0] == '@':
            split = tag_str.split('#')
            outline_list.append([int(split[0][1:]),'#' + split[1]])
        else:
            style_list.append(tag_str)

# Converts a string with bespoke markdown into a plaintext string and corresponding formatting information
def parse_markdown(str, default_color, default_outline):
    # array of 5-tuples (style, color, outline_weight, outline_color, text)
    string_data = []
    style = ['regular']
    color = [default_color]
    outline = [default_outline]
    # Matches any unescaped '<' or '>'
    for index, substr in enumerate(re.split(r'(?<!\\)[<>]', str)):
        # Odd outputs are always text, even is always formatting info
        if index % 2 == 0:
            final_style = style[-1]
            if (style.count('bold') and style.count('italic')):
                final_style = 'bold_italic'
            # Remove any escape characters left over
            string_data += [(final_style, color[-1], outline[-1][0], outline[-1][1], re.sub(r'(?<!\\)\\', '', substr))]
        else:
            manage_tags(substr, color, style, outline)
            
    # Remove any left over empty string sections
    string_data = [element for element in string_data if element[2] != '']
    return string_data


# Composite two images, where the first is larger than the second.
# canvas = PIL image object
# addition_dict = dict with path and offsets defined
# TODO: Add the ability to scale images, optionally
def composite_images(canvas, addition_dict):
    dest_offsets = get_attr_if_present(addition_dict, 'dest_offsets', [0,0])
    src_offsets = get_attr_if_present(addition_dict, 'source_offsets', [0,0])
    try:
        with Image.open(addition_dict['path']) as addition_image:
            canvas.alpha_composite(addition_image, tuple([int(offset) for offset in dest_offsets]), tuple([int(offset) for offset in src_offsets]))
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
    for style, color, outline_weight, outline_color, text_data in markdown_objects:
        substrings = text_data.split('\n')
        for idx, substr in enumerate(substrings):
            if (idx >= 1):
                txt_arr[-1].crop((0,0,x_offset+(outline_weight*2),font_size+(outline_weight*2)))
                txt_arr += [Image.new("RGBA", (5000,200),(0,0,0,0))]
                x_offset = 0
            draw = ImageDraw.Draw(txt_arr[-1])
            draw_box = draw.textbbox((x_offset,0), substr, font=fonts[style])
            draw.text((x_offset+outline_weight,0), substr, font=fonts[style], fill=outline_color, stroke_width=outline_weight)
            draw.text((x_offset+outline_weight,0), substr, color, font=fonts[style])
            txt_arr[-1] = draw_badges(txt_arr[-1], substr, fonts[style], x_offset, badge_dict)
            x_offset += draw_box[2]-draw_box[0]+outline_weight/2
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

def get_attr_if_present(dict, attr, default, blame=None):
    try:
        out = dict[attr]
    except KeyError:
        if blame:
            print(f"Attempted to get attribute {attr}, but it wasn't defined in {blame}.")
        out = default
    return out

def text_by_style(image, text, style_dict, badge_dict={}):
    return draw_text(image, text, 
                     style_dict['fonts'],
                     style_dict['bounding_box'], 
                     max_font_size=get_attr_if_present(style_dict, 'default_font_size', 88),
                     max_vertical_spacing=get_attr_if_present(style_dict, 'default_line_height', 88), 
                     align=get_attr_if_present(style_dict,'align', 'center'),
                     badge_dict=badge_dict,
                     default_color=get_attr_if_present(style_dict,'text_color', '#000000'),
                     default_outline=get_attr_if_present(style_dict,'outline', [0,'#000000']))

# Draws text in the canvas, converting between styles and adjusting size and spacing on the fly
# canvas = PIL Image object
# text = raw string data (to be passed to the markdown parser)
# font_files = (regular, bold, italic, bold-italic), all paths to their otf/ttf files
# bounding_box = (left, top, right, bottom), all in pixels from the top-left of the image
# max_font_size = largest font size to scale up to, in pixels.
# max_vertical_spacing = largest space between lines, in pixels.

def draw_text(canvas, text, font_files, bounding_box, max_font_size=33, max_vertical_spacing=50, align='center', badge_dict={}, default_color='#000000', default_outline=[0,'#000000']):
    markdown_objects = parse_markdown(text, default_color, default_outline)
    text_size = (bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1])
    image_lines = compose_text(markdown_objects, font_files, max_font_size, badge_dict=badge_dict)
    line_height = min(max_vertical_spacing, get_line_height(max_font_size, len(image_lines),text_size[1]))
    text_image = Image.new("RGBA", (5000,5000),(0,0,0,0))
    cursor_y = 0
    max_width = 0
    center_x = text_image.size[0] // 2
    for idx, line in enumerate(image_lines):
        line_bbox = line.getbbox()
        if line_bbox == None:
            continue
        cursor_y = idx*line_height
        if align == 'left':
            text_location = (center_x-text_size[0]//2,cursor_y)
        elif align == 'right':
            text_location = ((center_x+text_size[0]//2)-line_bbox[2],cursor_y)
        else:
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
    dest_corner = (bounding_box[0], bounding_box[1] + (text_size[1] - (cursor_y+line_height))//2)
    source_corner = ((text_image.size[0]-text_size[0])// 2, 0)
    canvas.alpha_composite(text_image, dest_corner,source_corner)
    return canvas

# Replace any {} strings with their corresponding data
def replace_data(obj, translation_table):
    if type(obj) == str:
        try:
            # Load as JSON if the resulting object is json,
            try:
                return json.loads(obj.format(**translation_table).replace('\'', '\"'))
            except KeyError as err:
                err.add_note(f'The template asked for variable {err}, but no matching definition was found in that location.')
                raise
        except json.decoder.JSONDecodeError:
            # Load as string otherwise
            return re.sub(r'[\"\']', '', obj.format(**translation_table))
    elif type(obj) == list:
        for idx, value in enumerate(obj):
            obj[idx] = replace_data(value, translation_table)
        return obj
    elif type(obj) == dict:
        for key, value in obj.items():
            obj[key] = replace_data(value, translation_table)
    return obj

def create_translation_table(obj, table, key_path):
    table[key_path] = json.dumps(obj)
    if type(obj) != dict:
        return table
    for key, value in obj.items():
        create_translation_table(value, table, key_path + ',' + key)
    return table


# TODO: Add support for default card types, in case of missing types
def generate_card(card):
    translation_table = {}
    translation_table = create_translation_table(card['template_info'], translation_table, 'template')
    translation_table = create_translation_table(card['config_info'], translation_table, 'config')
    translation_table = create_translation_table(card, translation_table, 'card')
    card['template_info'] = replace_data(card['template_info'], translation_table)
    with Image.new("RGBA", tuple(card['config_info']['image_size_px']),(0,0,0,0)) as card_image:
        try:
            for attribute_label, card_attribute in card['template_info']['data'][card['card_type'].lower()].items():
                show_if = get_attr_if_present(card_attribute,'show_if', [])
                show_equal = get_attr_if_present(card_attribute,'show_equal', [])
                show_not_equal = get_attr_if_present(card_attribute,'show_not_equal', [])
                is_continue = False
                for idx in range(len(show_if)):
                    if idx < len(show_not_equal) and show_if[idx] == show_not_equal[idx]:
                        is_continue = True
                    if idx < len(show_equal) and show_if[idx] != show_equal[idx]:
                        is_continue = True
                if is_continue: continue
                attribute_type = get_attr_if_present(card_attribute,'type', '', f'Template: {card["card_type"].lower()}: {attribute_label}')
                if attribute_type == 'image':
                    composite_images(card_image, card_attribute)
                if attribute_type == 'text':
                    badges = get_attr_if_present(card_attribute,'text_to_image', {})
                    text_by_style(card_image, get_attr_if_present(card_attribute,'content', 'ERR', f'Template: {card["card_type"].lower()}: {attribute_label}'), card_attribute, badges)
        except KeyError as err:
                err.add_note(f"""Sorry, this template doesn't recognize card type {err}.\nPlease ensure that the card type is spelled correctly in the template.\nIf it is, please choose a different template.\nFor template designers: Make sure that the card type in template_info.json is in lowercase.""")
                raise
    return card_image


def format_color_words(text):
    for key in stat_words:
        text = re.sub('\+([0-9]*) ' + key, '<bold> <' + stat_words[key] + '><@3#000000>' + "+\\1 " + key + '</@></#></bold>', text)
    return text

def format_bold_words(text):
    for word in bold_words:
        text = text.replace(word, '<bold>' + word + '</bold>')
    return text

def capitalize_important_words(text):
    for word in bold_words:
        uncapped = word.lower()
        text = text.replace(uncapped, word)
    return text


def format_common_text(text):
    text = capitalize_important_words(text)
    text = format_bold_words(text)
    text = format_color_words(text)
    return text
