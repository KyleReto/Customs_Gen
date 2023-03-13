import csv
import json
import unittest.mock as mock
from template_manager import generate_character, generate_exceed, generate_special, generate_ultra

# Code provided by Cobalt
def create_specials():

    csv_path = './assets/test.csv'
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        special_count = 0
        for row in csv_reader:
            if row[1] == 'Special':
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
                card.card_name = row[0]
                card.card_type = row[1]
                card.owner = row[2]
                card.copies = row[3]
                #TODO formatting for bolding and coloring

                #card.text_box = """Exceed Text
                #<bold>Bold text:</bold> Normal Text <italic>(Italic Text)</italic>
                #<bold><#0069ff>+0~1 Range</#0069ff>, <#0069ff>+2-3 Range</#0069ff>, <#b80000>+1 Power</#b80000>,
                #<#877400>-1 Speed</#877400>, <#7d2e81>+2 Armor</#7d2e81>, <#127a00>-4 Guard</#127a00></bold>"""

                card.text_box = row[4]

                #card.secondary_text_box = '''Boost 1 Text
                #<bold>Bold text:</bold> Normal Text <italic>(Italic Text)</italic>
                #This boost is continuous, and has 1 force cost'''

                card.secondary_text_box = row[15]
                card.cost = row[5]
                card.secondary_cost = row[11]
                if card.secondary_cost == '':
                    card.secondary_cost = '0'

                card.secondary_type = row[14]
                card.secondary_subtype = row[13]
                card.range = row[6]
                card.power = row[7]
                card.speed = row[8]
                card.armor = row[9]
                card.guard = row[10]
                card.secondary_name = row[12]
                
                card.template_info = template_info
                card.config_info = config_info
                special_count = special_count + 1
                generate_special(card, special_count).save('output/special' + str(special_count) + '.png')
                
                # End development code
            if row[1] == 'Character' or row[1] == 'Exceed':
                # Front code
                card = mock.Mock()
                template_path = './templates/street_fighter/'
                config_path = './config.json'
                f = open(template_path + 'template_info.json')
                template_info = json.load(f)
                f.close()
                f = open(config_path)
                config_info = json.load(f)
                f.close()

                card.card_name = row[0]
                card.text_box = row[4]
                card.cost = row[5]
                card.secondary_type = row[14]
                card.secondary_cost = row[11]
                card.owner = row[2]

                card.template_info = template_info
                card.config_info = config_info

                if row[1] == 'Character':
                    generate_character(card).save('output/front.png')
                else:
                    generate_exceed(card).save('output/back.png')
                # End front code

    return 0

create_specials()