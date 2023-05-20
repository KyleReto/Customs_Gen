from tkinter import *
from tkinter import filedialog
from automator import create_cards
from tkinter.ttk import Combobox
import json


parentFolder = "Customs_Gen/"

jsonFile = open("./config.json", "r") # Open the JSON file for reading
data = json.load(jsonFile) # Read the JSON into the buffer
jsonFile.close() # Close the JSON file

window = Tk()
window.title('Exceed Generator')
window.resizable(False, False)

csvPath = StringVar()
csvPath.set('Please select a csv file')

templatePath = StringVar()
templatePath.set('Please select the template folder')

outputPath = StringVar()
outputPath.set('output')

jsonOutputPath = StringVar()
jsonOutputPath.set('TTSOutput')

charImgPath = StringVar()
charImgPath.set('Please select the character image')

exceedImgPath = StringVar()
exceedImgPath.set('Please select the exceed image')

logoImgPath = StringVar()
logoImgPath.set('Please select the logo image')

attackImgPath = StringVar()
attackImgPath.set('No attack images set this session (using paths from previous session)')

progress = StringVar()


def updateJsonFile():
    ## Working with buffered content

    ## Save our changes to JSON file
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def openCSVFile():
    filepath = filedialog.askopenfilename(initialdir=".\\csv",
                                          title="Exceed Card Generator",
                                          filetypes=(("csv file", "*.csv"),
                                          ("all files", "*.*")))
    while parentFolder in filepath:
        filepath = filepath.split(parentFolder,1)[1]
    csvPath.set(filepath) 
    window.update_idletasks()

def openPicFile():
    filepath = filedialog.askopenfilename(initialdir=".\\character_images",
                                          title="Exceed Card Generator",
                                          filetypes=(("png", "*.png"),
                                                     ("jpg", "*.jpg"),
                                                     ("jpeg", "*.jpeg"),
                                          ("all files", "*.*")))
    while parentFolder in filepath:
        filepath = filepath.split(parentFolder,1)[1]
    return filepath

def fetchImgUsed(picNum):
    attackImgPath.set(data["images"]["card_art"][picNum]["path"])
    window.update_idletasks()

def setImgForAllStrikes():
    filepath = openPicFile()
    for i in range(10):
        data["images"]["card_art"][i]["path"] = filepath
        data["images"]["card_art"][i]["type"] = 'image'
    attackImgPath.set("Set all attack Images to " + filepath)
    window.update_idletasks()

def setImgForStrike(picNum):
    filepath = openPicFile()
    data["images"]["card_art"][picNum]["path"] = filepath
    data["images"]["card_art"][picNum]["type"] = 'image'
    attackImgPath.set("Set attack Image to " + filepath)
    window.update_idletasks()

def setCharImage(updatePath, toChange):
    filepath = openPicFile()
    data["images"][toChange]["path"] = filepath
    updatePath.set(filepath)
    window.update_idletasks()


def openTemplateFolder():
    folderPath = filedialog.askdirectory(initialdir=".\\templates",
                                         title="Exceed Card Generator")
    while parentFolder in folderPath:
        folderPath = folderPath.split(parentFolder,1)[1]
    templatePath.set(folderPath) 
    window.update_idletasks()

def openOutputFolder():
    folderPath = filedialog.askdirectory(initialdir=".\\output",
                                         title="Exceed Card Generator")
    while parentFolder in folderPath:
        folderPath = folderPath.split(parentFolder,1)[1]
    outputPath.set(folderPath) 
    window.update_idletasks()

def openTTSFolder():
    folderPath = filedialog.askdirectory(initialdir=".\\output",
                                         title="Exceed Card Generator")
    while parentFolder in folderPath:
        folderPath = folderPath.split(parentFolder,1)[1]
    jsonOutputPath.set(folderPath) 
    window.update_idletasks()


def generate_all_cards():

    updateJsonFile()

    #TODO: On release, put this in try block to notify user. It is easier to track error logs like this for now
    progress.set('Loading. Window will close automatically once complete.\nCheck the console for progress')
    window.update_idletasks()
    create_cards(csvPath.get(), templatePath.get(), outputPath.get(), jsonOutputPath.get(), CheckVar1.get(), CheckVar2.get())
    print('Finished')
    window.destroy()


    #try:

    #except Exception as err:
    #    progress.set('Ran into a fatal issue. \nEnsure you selected a csv file\nand that all strikes point to a picture file')
    #    print(err)
    #    window.update_idletasks()

column1Horz = 100
column2Horz = 400
column1height = 35
buttonbuffer = 40
labelbuffer = 25
column2height = 35
generatebuffer = 200
labelWidth = 45
checkboxBuffer = 25
checkboxAdjust = -150

currentCSVPath = Label(window, textvariable=csvPath, width=labelWidth, anchor="sw")
currentCSVPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

window.minsize(width=800, height=500)
csvButton = Button(text = "Select csv", command=openCSVFile)
csvButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentCharImgPath = Label(window, textvariable=charImgPath, width=labelWidth, anchor="sw")
currentCharImgPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

charImgButton = Button(text = "Select character image", command=lambda: (setCharImage(charImgPath, "character_image")))
charImgButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentexceedImgPath = Label(window, textvariable=exceedImgPath, width=labelWidth, anchor="sw")
currentexceedImgPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer


exceedImgButton = Button(text = "Select exceed image", command=lambda: (setCharImage(exceedImgPath, "exceed_image")))
exceedImgButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentlogoImgPath = Label(window, textvariable=logoImgPath, width=labelWidth, anchor="sw")
currentlogoImgPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer


logoImgButton = Button(text = "Select logo image", command=lambda: (setCharImage(logoImgPath, "character_logo")))
logoImgButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentAttackImgPath = Label(window, textvariable=attackImgPath, width=labelWidth, anchor="sw")
currentAttackImgPath.place(x=column2Horz, y=column2height)

column2height = column2height + labelbuffer

options=("Strike 1", "Strike 2", "Strike 3", "Strike 4", "Strike 5", "Strike 6", "Strike 7", "Strike 8", "Strike 9", "Strike 10")
cb=Combobox(window, values=options)
cb.place(x=column2Horz, y=column2height)

column2height = column2height + buttonbuffer

attackImgButton = Button(text = "Set Selected Attack Image", command=lambda: (setImgForStrike(options.index(cb.get()))))
attackImgButton.place(x=column2Horz, y=column2height)

column2height = column2height + buttonbuffer

fetchAttackImgButton = Button(text = "Fetch Selected Attack Image", command=lambda: (fetchImgUsed(options.index(cb.get()))))
fetchAttackImgButton.place(x=column2Horz, y=column2height)

column2height = column2height + buttonbuffer

setAllAttackImgButton = Button(text = "Select an Image to use for all attacks", command=lambda: (setImgForAllStrikes()))
setAllAttackImgButton.place(x=column2Horz, y=column2height)

column2height = column2height + generatebuffer

column2height = column2height + checkboxAdjust
CheckVar1 = IntVar()
CheckVar2 = IntVar()
C1 = Checkbutton(window, text = "Upload to Imgur", variable = CheckVar1, onvalue = 1, offvalue = 0, height=0, width = 0)
C2 = Checkbutton(window, text = "Create character json at output (eases updating character)", variable = CheckVar2, onvalue = 1, offvalue = 0, height=0, width = 0)
C1.place(x=column2Horz, y=column2height)
column2height = column2height + checkboxBuffer
C2.place(x=column2Horz, y=column2height)
column2height = column2height + generatebuffer

currentTemplatePath = Label(window, textvariable=templatePath, width=labelWidth, anchor="sw")
currentTemplatePath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

templateButton = Button(text = "Select template folder", command=openTemplateFolder)
templateButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentOutputPath = Label(window, textvariable=outputPath, width=labelWidth, anchor="sw")
currentOutputPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

outputButton = Button(text = "Change output folder", command=openOutputFolder)
outputButton.place(x=column1Horz, y=column1height)

column1height = column1height + buttonbuffer

currentTTSOutputPath = Label(window, textvariable=jsonOutputPath, width=labelWidth, anchor="sw")
currentTTSOutputPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

jsonOutputButton = Button(text = "Change TTS json Output Folder", command=openTTSFolder)
jsonOutputButton.place(x=column1Horz, y=column1height)


column2height = column2height + checkboxAdjust

Loading = Label(window, textvariable=progress, width=labelWidth, anchor="sw")
Loading.place(x=column2Horz, y=column2height)

column2height = column2height + labelbuffer

generate = Button(text = "Generate Images", command=generate_all_cards)
generate.place(x=column2Horz, y=column2height)




window.mainloop()
