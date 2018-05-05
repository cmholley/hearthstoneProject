import json
import constants
import os
import time
from pymongo import MongoClient

'''
This script uses a .json file taken from https://api.hearthstonejson.com/v1/24118/enUS/cards.json
This file is a list of all hearthstone cards. This script filters the cards in that list to only 
cards used in the games present in the data set. It also trims un-needed data and inserts the results
into the "cards" mongo db collection at localhost
'''

def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards
    gamesDb = db.rankedGames

    #Drop existing cards to prevent duplicates
    cardsDb.drop()

    #Open json data of cards
    cardsFileData = {}
    with open(constants.CARDS_JSON_LOCATION,'r') as infile:
        cardsFile = json.load(infile)

    #Build dictionary from list in json file
    for card in cardsFile:
        id = card.get("id")
        cardsFileData[id] = card

    gamesData = list(gamesDb.find())
    cardData = {}
    classes = []


    # Takes a card structure from the hearthstonejson cards.json file and returns a simplified structure for the project
    def cardFilter(inputCard):
        card = {}
        card["cardClass"] = inputCard.get("cardClass").capitalize()
        card["name"] = inputCard.get("name")
        card["type"] = inputCard.get("type")
        card["rarity"] = inputCard.get("rarity")
        card["id"] = inputCard.get("id")

        return card

    #For every game, check each card in the card history
    for game in gamesData:
        for cardObj in game.get("card_history"):
            card = cardObj.get("card")
            id = card.get("id")
            #If this card hasn't been recorded, record it
            if id not in cardData:
                #Filter out the unneccessary data
                inputCard = cardsFileData[id]
                cardData[id] = cardFilter(inputCard)

    #Insert cards
    vertexIdCounter = 0
    for cardKey in cardData:
        card = cardData[cardKey]
        card["vertexId"] = vertexIdCounter
        vertexIdCounter += 1
        cardsDb.insert(card);

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()
