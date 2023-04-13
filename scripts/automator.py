import json
import csv
from template_manager import generate_card
from template_manager import format_common_text
from PIL import Image, ImageOps
from imgur_upload import *
from TTSGenerator import *
import tkinter as tk
from tkinter import Canvas, PhotoImage, Label
from PIL import Image, ImageTk


#Code by Michael Bowling/Alkaroth 
##This script reads an imported csv file and continuously calls the image generator with the correct parameters
#For now, this script is also in charge of generating the TTS Json.




def concat_images(image_paths, size, shape=None):
    # Open images and resize them
    width, height = size
    images = map(Image.open, image_paths)
    images = [ImageOps.fit(image, size, Image.ANTIALIAS) 
              for image in images]
    
    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    image_size = (width * shape[1], height * shape[0])
    image = Image.new('RGB', image_size)
    
    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = width * col, height * row
            idx = row * shape[1] + col
            try:
                image.paste(images[idx], offset)
            except:
                pass
    
    return image


def create_cards(csvPath, templatePath, outputPath):

    #TODO allow pointing to Normals Deck
    jsonFile = open("./normals/Seventh_Cross/Normals Deck.json", "r") # Open the JSON file for reading
    ttsData = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    char_name = "Character"
    charImgPath = ""
    exceedImgPath = ""
    csv_path = csvPath
    StrikeImages = []



    local = True
    test = False



    cardList = []
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        
        # used for hacky workaround on config structure
        tmp_idx = 0
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
            if card["cost"] == ' ':
                card["cost"] = ''
            card["secondary_cost"] = row[11]
            if card["secondary_cost"] == '':
                card["secondary_cost"] = '0'

            card["secondary_type"] = row[14]
            card["secondary_subtype"] = row[13]
            card["range"] = row[6].replace("~", "-")
            card["power"] = row[7]
            card["speed"] = row[8]

            card["armor"] = row[9]
            card["guard"] = row[10]

            if card["armor"] == " ":
                card["armor"] = ""
            if card["guard"] == " ":
                card["guard"] = ""

            card["secondary_name"] = row[12]
            
            card["template_info"] = template_info
            card["config_info"] = config_info
            
            savePath = outputPath + '/' + row[0] + '.png'
            #Apparently we need to check for new line characters here
            savePath = savePath.replace("\n", " ")
            # hacky workaround on config structure
            card["config_info"]['images']['card_art'] = card["config_info"]['images']['card_art'][tmp_idx]

            if row[1] == 'Special' or row[1] == 'Ultra':
                tmp_idx += 1
                generate_card(card).save(savePath)
                StrikeImages.append(savePath)

                if (local):
                    AddStrikeToLocalTts(ttsData, char_name, card, savePath)
                cardList.append(card)
                print("Generated " + row[0])


            elif row[1] == 'Character':
                char_name = row[0]
                generate_card(card).save(savePath)
                charImgPath = savePath
                print("Generated " + row[0])


            elif row[1] == 'Exceed':
                card["card_name"] = char_name
                savePath = outputPath + '/' + char_name + '_Exceed.png'
                #Apparently we need to check for new line characters here
                savePath = savePath.replace("\n", " ")
                generate_card(card).save(savePath)
                exceedImgPath = savePath
                print("Generated " + row[0])
            
    
    
    if (test):
        grid = concat_images(StrikeImages, (750, 1024), (2,4))
        img= grid.resize((1500,1024), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(img)
        
        root = tk.Toplevel()
        root.geometry("1500x1024")
        root.title("Image on backGround")
        root.resizable(True, True)
        display = Label(root, image=pic)
        display.pack()
        root.mainloop()
    elif(local):
        TtsAddCharacterLocal(ttsData, char_name, charImgPath, exceedImgPath)
        generate_tts_json(ttsData, char_name, outputPath) 
    else: #We are uploading to Imgur and using the link for the TTS
        gridCards = concat_images(StrikeImages, (750, 1024), (2,4))
        gridSavePath = outputPath + '/' + char_name + 'Grid.jpg'
        gridCards.save(gridSavePath, 'JPEG')

        ImagesToUpload = [gridSavePath, charImgPath, exceedImgPath]
        UploadedLinks = upload_images(ImagesToUpload, char_name)

        decklink = UploadedLinks[0]
        charLink = UploadedLinks[1]
        exceedLink = UploadedLinks[2]

        TtsSyncToUpload(ttsData, char_name, decklink, cardList, charLink, exceedLink)
        generate_tts_json(ttsData, char_name, outputPath) 
   
    return 0