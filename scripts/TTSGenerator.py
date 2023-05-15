
import json

deckNum = 1
gridWidth = 4
gridHeight = 2

# Each custom deck holds a grid image of custom cards
# Since we are using individual images, we need a custom deck
# for each card generated. This is only a reference; we will still
# end with just a single deck object
def TtsGenerateCustomDeck(ttsData, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):
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

    return customDeck

def TtsAddLocalStrikeToCustomDeck(ttsData, refData, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):

    customDeck = TtsGenerateCustomDeck(ttsData, imgPath, backPath)

    ttsData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    refData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    return deckNum

def TtsAddLocalCharToCustomDeck(ttsData, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):
    customDeck = TtsGenerateCustomDeck(ttsData, imgPath, backPath)

    ttsData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    return deckNum


def TtsAddDeckID(ttsData, deckNum):
    #For reference on why we multiply by 100, read this article
    #https://clementespeute.com/blog/tabletop-simulator-deck-format/
    ttsData["ObjectStates"][0]["DeckIDs"].append(deckNum*100)

def TtsAddLocalContainedCard(ttsData, deckNum, charName, card):
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
    contained_card["CardID"] =  deckNum*100
    ttsData["ObjectStates"][0]["ContainedObjects"].append(contained_card)

def TtsAddLocalContainedCharacter(ttsData, deckNum, charName):
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

    

def AddStrikeToLocalTts(ttsData, refDeck, charName, card, imgPath):

    #Add Custom Decks
    deckID = TtsAddLocalStrikeToCustomDeck(ttsData, refDeck, imgPath)
    
    for i in range(int(card["copies"])):
        #Add DeckID
        TtsAddDeckID(ttsData, deckID)

        #Add Contained Objects
        TtsAddLocalContainedCard(ttsData, deckID, charName, card)

    TtsAddDeckID(refDeck, deckID)


    TtsAddLocalContainedCard(refDeck, deckID, charName, card)


    return 0

def AddUniqueToLocalTts(ttsData, charName, card, imgPath):

    #Add Custom Decks
    deckID = TtsAddLocalCharToCustomDeck(ttsData, imgPath)
    
    for i in range(int(card["copies"])):
        #Add DeckID
        TtsAddDeckID(ttsData, deckID)

        #Add Contained Objects
        TtsAddLocalContainedCard(ttsData, deckID, charName, card)
    return 0





def TtsAddCharacterLocal(ttsData, charName, charImgPath, exceedImgPath):
    deckID = TtsAddLocalCharToCustomDeck(ttsData, charImgPath, exceedImgPath)
    TtsAddDeckID(ttsData, deckID)
    TtsAddLocalContainedCharacter(ttsData, deckID, charName)




def TtsCreateCustomDeckForGrid(imgPath, backPath):
    # each custom deck requires its own ID
    global deckNum
    deckNum = deckNum + 1

    customDeck = {
          "FaceURL": imgPath,
          "BackURL": backPath,
          "NumWidth": gridWidth,
          "NumHeight": gridHeight,
          "BackIsHidden": True,
          "UniqueBack": False,
          "Type": 0
        }
    return customDeck

def TtsAddStrikeDeckForGrid(ttsData, refDeck, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):
    customDeck = TtsCreateCustomDeckForGrid(imgPath, backPath)

    ttsData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    refDeck["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    return deckNum


def TtsAddUniqueDeckForGrid(ttsData, imgPath, backPath = "https://i.imgur.com/igYZhPh.png"):
    customDeck = TtsCreateCustomDeckForGrid(imgPath, backPath)

    ttsData["ObjectStates"][0]["CustomDeck"][deckNum] = customDeck
    return deckNum

def TtsAddGridContainedCard(ttsData, cardNum, deckNum, card):
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
          "Nickname": card["card_name"],
          "Description": card["card_name"],
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
          "CardID": cardNum,
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
    elif card["card_type"] == "Unique":
        nickname += " (C)"
    contained_card["Nickname"] = nickname
    
    customDeck = ttsData["ObjectStates"][0]["CustomDeck"][deckNum]
    contained_card["CustomDeck"][deckNum] = customDeck
    ttsData["ObjectStates"][0]["ContainedObjects"].append(contained_card)

def TtsAddDeckIDForGrid(ttsData, deckID, cardNum):
    #For reference on why we multiply by 100, read this article
    #https://clementespeute.com/blog/tabletop-simulator-deck-format/
    ttsData["ObjectStates"][0]["DeckIDs"].append(deckID)


def addUploadedCharCard(ttsData, char_name, charLink, exceedLink):
    deckID = TtsAddLocalStrikeToCustomDeck(ttsData, charLink, exceedLink)
    TtsAddDeckID(ttsData, deckID)
    TtsAddLocalContainedCharacter(ttsData, deckID, char_name)


def TTSSyncStrikesToUpload(ttsData, refDeck, decklink, cardList):
    deckNum = TtsAddStrikeDeckForGrid(ttsData, refDeck, decklink)
    cardNum= 0
    for card in cardList:
        cardID = deckNum*100 + cardNum
        for i in range(int(card["copies"])):
            TtsAddDeckIDForGrid(ttsData, cardID, cardNum)
            TtsAddGridContainedCard(ttsData, cardID, deckNum, card)
        TtsAddDeckIDForGrid(refDeck, cardID, cardNum)
        TtsAddGridContainedCard(refDeck, cardID, deckNum, card)
        cardNum = cardNum + 1

def TTSSyncUniqueToUpload(ttsData, decklink, cardList):
    deckNum = TtsAddUniqueDeckForGrid(ttsData, decklink)
    cardNum= 0
    for card in cardList:
        cardID = deckNum*100 + cardNum
        for i in range(int(card["copies"])):
            TtsAddDeckIDForGrid(ttsData, cardID, cardNum)
            TtsAddGridContainedCard(ttsData, cardID, deckNum, card)
        cardNum = cardNum + 1

def TtsSyncToUpload(ttsData, refDeck, char_name, decklink, cardList, uniquelink, uniqueCards, charLink, exceedLink):
    TTSSyncStrikesToUpload(ttsData, refDeck, decklink, cardList)
    if (uniqueCards.__len__ != 0):
        TTSSyncUniqueToUpload(ttsData, uniquelink, uniqueCards)
    addUploadedCharCard(ttsData, char_name, charLink, exceedLink)

def generate_tts_json(ttsData, refDeck, charName, outputPath):
    jsonSavePath = outputPath + '/' + charName + ' Deck.json'
    #Apparently we need to check for new line characters here
    jsonSavePath = jsonSavePath.replace("\n", " ")
    jsonFile = open(jsonSavePath, "w+")
    jsonFile.write(json.dumps(ttsData))
    jsonFile.close()


    #Adds a ref file. Currently bugged where the last card doesnt load correctly?
    
    #jsonSavePath = outputPath + '/' + charName + ' Reference.json'
    #Apparently we need to check for new line characters here
    #jsonSavePath = jsonSavePath.replace("\n", " ")
    #jsonFile = open(jsonSavePath, "w+")
    #jsonFile.write(json.dumps(refDeck))
    #jsonFile.close()
