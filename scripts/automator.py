import json
import csv
from template_manager import generate_card
from template_manager import format_common_text



deckNum = 1

# Each custom deck holds a grid image of custom cards
# Since we are using individual images, we need a custom deck
# for each card generated. This is only a reference; we will still
# end with just a single deck object
def tts_add_custom_deck(ttsData, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):
    # each custom deck requires its own ID
    global deckNum
    deckNum = deckNum + 1

    customDeck = {
          "FaceURL": imgPath,
          "BackURL": backPath,
          "NumWidth": 1,
          "NumHeight": 1,
          "BackIsHidden": True,
          "UniqueBack": False,
          "Type": 0
        }

    ttsData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    return deckNum



def tts_add_deckID(ttsData, deckNum):
    #For reference on why we multiply by 100, read this article
    #https://clementespeute.com/blog/tabletop-simulator-deck-format/
    ttsData["ObjectStates"][0]["DeckIDs"].append(deckNum*100)

def tts_add_contained_card(ttsData, deckNum, charName, card):
    #Note: I am not sure what many of these do. Some of these values
    # are discarded since card is used in deck as well
    contained_card = {
          "Name": "CardCustom",
          "Transform": {
            "posX": 0,
            "posY": 0,
            "posZ": 0,
            "rotX": 0,
            "rotY": 0,
            "rotZ": 0,
            "scaleX": 1.25,
            "scaleY": 1.0,
            "scaleZ": 1.25
          },
          "Nickname": "Block (N)",
          "Description": charName,
          "GMNotes": "",
          "Memo": "15",
          "ColorDiffuse": {
            "r": 0.58431375,
            "g": 0.0,
            "b": 0.7019608
          },
          "LayoutGroupSortIndex": 0,
          "Value": 0,
          "Locked": False,
          "Grid": True,
          "Snap": True,
          "IgnoreFoW": False,
          "MeasureMovement": False,
          "DragSelectable": True,
          "Autoraise": True,
          "Sticky": True,
          "Tooltip": False,
          "GridProjection": False,
          "HideWhenFaceDown": True,
          "Hands": True,
          "CardID": 107,
          "SidewaysCard": False,
          "CustomDeck": {
          },
          "LuaScript": "",
          "LuaScriptState": "",
          "XmlUI": ""
        }
    nickname = card["card_name"]
    if card["card_type"] == "Special":
        nickname += " (S)"
    elif card["card_type"] == "Ultra":
        nickname += " (U)"
    contained_card["Nickname"] = nickname
    
    customDeck = ttsData["ObjectStates"][0]["CustomDeck"][deckNum]
    contained_card["CustomDeck"][deckNum] = customDeck
    ttsData["ObjectStates"][0]["ContainedObjects"].append(contained_card)

def tts_add_contained_character(ttsData, deckNum, charName):
    #Note: I am not sure what many of these do. Some of these values
    # are discarded since card is used in deck as well
    contained_card = {
          "Name": "CardCustom",
          "Transform": {
            "posX": 0,
            "posY": 0,
            "posZ": 0,
            "rotX": 0,
            "rotY": 0,
            "rotZ": 0,
            "scaleX": 1.25,
            "scaleY": 1.0,
            "scaleZ": 1.25
          },
          "Nickname": "Block (N)",
          "Description": charName,
          "GMNotes": "",
          "Memo": "15",
          "ColorDiffuse": {
            "r": 0.58431375,
            "g": 0.0,
            "b": 0.7019608
          },
          "LayoutGroupSortIndex": 0,
          "Value": 0,
          "Locked": False,
          "Grid": True,
          "Snap": True,
          "IgnoreFoW": False,
          "MeasureMovement": False,
          "DragSelectable": True,
          "Autoraise": True,
          "Sticky": True,
          "Tooltip": False,
          "GridProjection": False,
          "HideWhenFaceDown": True,
          "Hands": True,
          "CardID": 107,
          "SidewaysCard": False,
          "CustomDeck": {
          },
          "LuaScript": "",
          "LuaScriptState": "",
          "XmlUI": ""
        }
    nickname = charName + " (C)"
    contained_card["Nickname"] = nickname
    
    customDeck = ttsData["ObjectStates"][0]["CustomDeck"][deckNum]
    contained_card["CustomDeck"][deckNum] = customDeck
    ttsData["ObjectStates"][0]["ContainedObjects"].append(contained_card)

def add_strike_to_tts(ttsData, charName, card, imgPath):

    #Add Custom Decks
    deckID = tts_add_custom_deck(ttsData, imgPath)
    
    for i in range(int(card["copies"])):
        #Add DeckID
        tts_add_deckID(ttsData, deckID)

        #Add Contained Objects
        tts_add_contained_card(ttsData, deckID, charName, card)


    return 0


def tts_add_character(ttsData, charName, charImgPath, exceedImgPath):
    deckID = tts_add_custom_deck(ttsData, charImgPath, exceedImgPath)
    tts_add_deckID(ttsData, deckID)
    tts_add_contained_character(ttsData, deckID, charName)

def generate_tts_json(ttsData, charName, outputPath):
    jsonFile = open(outputPath + '/' + charName + 'Deck.json', "w+")
    jsonFile.write(json.dumps(ttsData))
    jsonFile.close()

def create_cards(csvPath, templatePath, outputPath):

    #TODO allow pointing to Normals Deck
    jsonFile = open("./normals/Seventh_Cross/Normals Deck.json", "r") # Open the JSON file for reading
    ttsData = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    char_name = "Character"
    charImgPath = ""
    exceedImgPath = ""
    csv_path = csvPath
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        


        for row in csv_reader:
            card = {}
            config_path = './config.json'
            f = open(templatePath + '/template_info.json', encoding='utf-8')
            template_info = json.load(f)
            f.close()
            f = open(config_path, encoding='utf-8')
            config_info = json.load(f)
            f.close()

            card["card_name"] = row[0]
            card["card_type"] = row[1]
            card["owner"] = row[2]
            card["copies"] = row[3]
            
            
            card["text_box"] = format_common_text(row[4])

            
            card["secondary_text_box"] = format_common_text(row[15])
            card["cost"] = row[5]
            card["secondary_cost"] = row[11]
            if card["secondary_cost"] == '':
                card["secondary_cost"] = '0'

            card["secondary_type"] = row[14]
            card["secondary_subtype"] = row[13]
            card["range"] = row[6]
            card["power"] = row[7]
            card["speed"] = row[8]
            card["armor"] = row[9]
            card["guard"] = row[10]
            card["secondary_name"] = row[12]
            
            card["template_info"] = template_info
            card["config_info"] = config_info
            
            savePath = outputPath + '/' + row[0] + '.png'
            if row[1] == 'Special' or row[1] == 'Ultra':
                
                generate_card(card).save(savePath)
                add_strike_to_tts(ttsData, char_name, card, savePath)
                print("Generated " + row[0])

            elif row[1] == 'Character':
                char_name = row[0]
                generate_card(card).save(savePath)
                charImgPath = savePath
                print("Generated " + row[0])
            elif row[1] == 'Exceed':
                card["card_name"] = char_name
                savePath = outputPath + '/' + char_name + '_Exceed.png'
                generate_card(card).save(savePath)
                exceedImgPath = savePath
                print("Generated " + row[0])
            


            # End front code
    tts_add_character(ttsData, char_name, charImgPath, exceedImgPath)
    generate_tts_json(ttsData, char_name, outputPath) 
   
    return 0