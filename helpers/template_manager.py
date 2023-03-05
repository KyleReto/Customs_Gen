from PIL import Image
import json
import unittest.mock as mock

# Development code
card = mock.Mock()
template_path = './templates/street_fighter/'
f = open(template_path + 'template_info.json')
template_info = json.load(f)
f.close()
card.name = "Character Name"
card.card_type = "Character"
card.owner = None
card.copies = 1
card.text_box = """Character text
Bold text: Normal Text (Italic Text)
This character can  -- Critical for 2 Gauge
(\" --\" = crit symbol)"""
card.cost = 3
card.secondary_cost = 2
card.secondary_type = 'Critical'
# End development code

# Composite two images, where the first is larger than the second.
# canvas = PIL image object
# addition_dict = dict from template_info.json
def composite_images(canvas, image_key):
    try:
        addition_dict = template_info["images"][image_key]
        with Image.open(template_path + addition_dict['path']) as addition_image:
            canvas.alpha_composite(addition_image, (addition_dict['x_offset'], addition_dict['y_offset']), (0,0))
    except KeyError:
        print(f"Couldn't find a definition for \"{image_key}\". "\
              "If an image for this object exists in this template, "\
              "make sure that it's defined correctly in template_info.json.")
    except FileNotFoundError:
        print(f"Couldn't find a file at path \"{template_info['images'][image_key]['path']}.\" "\
              "If an image for this object exists in this template, "\
              "make sure that it's defined correctly in template_info.json.")
    return canvas

def generate_character(card):
    with Image.open(template_path + template_info["images"]["character_frame"]["path"]) as frame:
        composite_images(frame, "exceed_flip")
        composite_images(frame, "character_critical")
        composite_images(frame, "critical_icon")
        frame.show()

generate_character(card)