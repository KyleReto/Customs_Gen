from tkinter import *
from tkinter import filedialog
from automator import create_cards_full_config
from tkinter.ttk import Combobox
import json


parentFolder = "Customs_Gen/"



window = Tk()
window.title('Exceed Generator')
window.resizable(False, False)

configPath = StringVar()
configPath.set('Please select the json config file')

progress = StringVar()

def updateJsonFile():

    configString = configPath.get()
    jsonFile = open(configString, "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    ## Working with buffered content

    ## Save our changes to JSON file
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def openConfigFile():
    filepath = filedialog.askopenfilename(initialdir=".\\",
                                          title="Exceed Card Generator",
                                          filetypes=(("json file", "*.json"),
                                          ("all files", "*.*")))
    while parentFolder in filepath:
        filepath = filepath.split(parentFolder,1)[1]
    configPath.set(filepath) 
    window.update_idletasks()

def generate_all_cards():

    updateJsonFile()

    #TODO: On release, put this in try block to notify user. It is easier to track error logs like this for now
    progress.set('Loading. Window will close automatically once complete.\nCheck the console for progress')
    window.update_idletasks()
    create_cards_full_config()
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

currentConfigPath = Label(window, textvariable=configPath, width=labelWidth, anchor="sw")
currentConfigPath.place(x=column1Horz, y=column1height)

column1height = column1height + labelbuffer

window.minsize(width=800, height=500)
configButton = Button(text = "Select csv", command=openConfigFile)
configButton.place(x=column1Horz, y=column1height)

Loading = Label(window, textvariable=progress, width=labelWidth, anchor="sw")
Loading.place(x=column2Horz, y=column2height)

column2height = column2height + labelbuffer

generate = Button(text = "Generate Images", command=generate_all_cards)
generate.place(x=column2Horz, y=column2height)

window.mainloop()
