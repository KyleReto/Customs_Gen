import pyimgur
import configparser
import webbrowser
import os
import datetime


def upload_img(path):
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'auth.txt')

    config = configparser.ConfigParser()
    config.read(initfile)

    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')



    im = pyimgur.Imgur(client_id=client_id, client_secret=client_secret)
    auth_url = im.authorization_url('pin')
    webbrowser.open(auth_url)
    pin = input("What is the pin? ") # Python 3x
    #pin = raw_input("What is the pin? ") # Python 2x
    im.exchange_pin(pin)

    
    uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
    #print(uploaded_image.title)
    #print(uploaded_image.link)
    #print(uploaded_image.size)
    #print(uploaded_image.type)
    return uploaded_image.link





def upload_images(pathArray, charName):
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'auth.txt')

    config = configparser.ConfigParser()
    config.read(initfile)

    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')



    im = pyimgur.Imgur(client_id=client_id, client_secret=client_secret)
    auth_url = im.authorization_url('pin')
    webbrowser.open(auth_url)
    pin = input("What is the pin? ") # Python 3x
    #pin = raw_input("What is the pin? ") # Python 2x
    im.exchange_pin(pin)

    albumTitle = "Exceed Auto generator, character " + charName + ", Date/Time: " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    newAlbum = pyimgur.Imgur.create_album(self=im, title=albumTitle)
    returnArray = []
    for path in pathArray:
        uploaded_image = im.upload_image(path, title="Uploaded with PyImgur", album=newAlbum)
        returnArray.append(uploaded_image.link)

    return returnArray


