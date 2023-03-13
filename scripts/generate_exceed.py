from tkinter import *
from tkinter import filedialog
from template_manager import create_cards
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
                                          ("all files", "*.*")))
    while parentFolder in filepath:
        filepath = filepath.split(parentFolder,1)[1]
    return filepath

def fetchImgUsed(picNum):
    attackImgPath.set(data["images"]["card_art"][picNum]["path"])
    window.update_idletasks()

def setImgForAllStrikes():
    filepath = openPicFile()
    for i in range(9):
        data["images"]["card_art"][i]["path"] = filepath
    attackImgPath.set("Set all attack Images to " + filepath)
    window.update_idletasks()

def setImgForStrike(picNum):
    filepath = openPicFile()
    data["images"]["card_art"][picNum]["path"] = filepath
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


def open_py_file():

    updateJsonFile()

    try:
        progress.set('Loading. Window will close automatically once complete.\nCheck the console for progress')
        window.update_idletasks()
        create_cards(csvPath.get(), templatePath.get())
        print('Finished')
        window.destroy()
    except Exception as err:
        progress.set('Ran into a fatal issue. \nEnsure you selected a csv file\nand that all strikes point to a picture file')
        print(err)
        window.update_idletasks()


currentCSVPath = Label(window, textvariable=csvPath)
currentCSVPath.pack()

window.minsize(width=400, height=400)
csvButton = Button(text = "Select csv", command=openCSVFile)
csvButton.pack()


currentCharImgPath = Label(window, textvariable=charImgPath)
currentCharImgPath.pack()

charImgButton = Button(text = "Select character image", command=lambda: (setCharImage(charImgPath, "character_image")))
charImgButton.pack()


currentexceedImgPath = Label(window, textvariable=exceedImgPath)
currentexceedImgPath.pack()


exceedImgButton = Button(text = "Select exceed image", command=lambda: (setCharImage(exceedImgPath, "exceed_image")))
exceedImgButton.pack()

currentlogoImgPath = Label(window, textvariable=logoImgPath)
currentlogoImgPath.pack()


logoImgButton = Button(text = "Select logo image", command=lambda: (setCharImage(logoImgPath, "character_logo")))
logoImgButton.pack()


currentAttackImgPath = Label(window, textvariable=attackImgPath)
currentAttackImgPath.pack()

options=("Strike 1", "Strike 2", "Strike 3", "Strike 4", "Strike 5", "Strike 6", "Strike 7", "Strike 8", "Strike 9", "Strike 10")
cb=Combobox(window, values=options)
cb.pack()


attackImgButton = Button(text = "Set Selected Attack Image", command=lambda: (setImgForStrike(options.index(cb.get()))))
attackImgButton.pack()

fetchAttackImgButton = Button(text = "Fetch Selected Attack Image", command=lambda: (fetchImgUsed(options.index(cb.get()))))
fetchAttackImgButton.pack()

setAllAttackImgButton = Button(text = "Use selected Image for all strikes", command=lambda: (setImgForAllStrikes()))
setAllAttackImgButton.pack()



currentTemplatePath = Label(window, textvariable=templatePath)
currentTemplatePath.pack()

templateButton = Button(text = "Select template folder", command=openTemplateFolder)
templateButton.pack()


Loading = Label(window, textvariable=progress)
Loading.pack()

generate = Button(text = "Generate Images", command=open_py_file)
generate.pack()




window.mainloop()
