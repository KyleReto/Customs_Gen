from PIL import Image, ImageFont, ImageDraw
import json
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
card.name = "Character Name"
card.card_type = "Character"
card.owner = None
card.copies = 1
card.text_box = """Character text
**Bold text:** Normal Text *(Italic Text)*
This character can ** -- Critical** for ***2 Gauge***
*(\" --\" = crit symbol)*"""
card.cost = 3
card.secondary_cost = 2
card.secondary_type = 'Critical'
card.template_info = template_info
card.config_info = config_info
# End development code

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

# Draws text in the canvas, converting between styles and adjusting size and spacing on the fly
# canvas = PIL Image object
# text = string
# font_files = (regular, bold, italic, bold-italic), all paths to their otf/ttf files
# bounding_box = (left, top, right, bottom), all in pixels from the top-left of the image
# max_font_size = largest font size to scale up to, in pixels.
# max_vertical_spacing = largest space between lines, in pixels.
def draw_text(canvas, text, font_files, bounding_box, max_font_size=999, max_vertical_spacing=999, align='center'):
    fonts = [ImageFont.truetype(font_file, 33) for font_file in font_files]
    text_size = (bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1])
    with Image.new("RGBA", text_size,(0,0,0,0)) as txt:
        draw = ImageDraw.Draw(txt)
        draw.text((0,0), text, fill=(0,0,0,255), font=fonts[0], align=align)
        canvas.alpha_composite(txt, (bounding_box[0],bounding_box[1]),(0,0))
        return canvas

def generate_character(card):
    template_images = card.template_info["images"]
    config_images = card.config_info["images"]
    fonts = [card.template_info['fonts']['effect_regular'],
             card.template_info['fonts']['effect_bold'],
             card.template_info['fonts']['effect_italic'],
             card.template_info['fonts']['effect_bold_italic']]

    with Image.new("RGBA", tuple(card.config_info['image_size_px']),(0,0,0,0)) as card_image:
        composite_images(card_image, template_images["character_background"])
        composite_images(card_image, config_images["character_image"])
        composite_images(card_image, template_images["character_frame"])
        composite_images(card_image, template_images["character_critical"])
        composite_images(card_image, template_images["critical_icon"])
        composite_images(card_image, template_images["exceed_flip"])
        draw_text(card_image, card.text_box, fonts, (54,758,695,990))
        return card_image

generate_character(card).show()