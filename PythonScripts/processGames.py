import constants
import os
import time
from pymongo import MongoClient

'''
This script is designed to process the documents in mongo in the rankedGames collection.
It will go in and replace each card in the card history with the object id of the card.
This ties the documents together explicitly instead of through an intermediary id, preventing desynchronized data
'''
def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards
    gamesDb = db.rankedGames


    gamesList = list(gamesDb.find())
    #Create card dictionary
    cardsList = list(cardsDb.find())
    cardsData = {}
    for card in cardsList:
        id = card.get("id")
        cardsData[id] = card

    for game in gamesList:
        deleteList = []
        for i in range(0,len(game.get("card_history"))):
            cardObj = game.get("card_history")[i]
            card = cardObj.get("card")
            id = card.get("id")
            realCard = cardsData[id]
            type = realCard.get("type")
            #Ignore heros, hero powers and the coin (GAME_005)
            if type == "HERO_POWER" or type == "HERO" or id == "GAME_005":
                deleteList.append(i)
            else:
                realCardObjId = realCard.get("_id")
                cardObj["card"] = realCardObjId

        deleteList.sort()
        counter = 0
        for i in deleteList:
            del game["card_history"][i-counter]
            counter += 1
        gameId = game.get("_id")
        gamesDb.update_one({"_id": gameId},{"$set": game})


def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()
