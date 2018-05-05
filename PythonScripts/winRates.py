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
    edgesDb = db.edges

    gamesList = list(gamesDb.find())
    cardsList = list(cardsDb.find())
    edgesList = list(edgesDb.find())

    edgesData = {}
    cardsData = {}

    #Create card dictionary
    for card in cardsList:
        objectId = card.get("_id")
        cardsData[objectId] = card

    #Create edge dictionary
    for edge in edgesList:
        edgeName = edge.get("edgeName")
        edgesData[edgeName] = edge

    '''
    First we will compute the card win rates. We loop through each game,
    building a list of the cards played by each player without duplicates.
    For each card in both lists, we add 1 to the gameCount variable. For
    the winning set of cards, we add one to the winCount variable. At the end,
    the win rate is calculated by winCount/gameCount
    '''

    for game in gamesList:
        myCards = []
        oppCards = []
        result = game.get("result")
        for cardObj in game.get("card_history"):
            if cardObj.get("player") == "me":
                myCards.append(cardObj.get("card"))
            else:
                oppCards.append(cardObj.get("card"))
        if result == "win":
            win = True
        else:
            win = False
        #We are only interested in cards each side played uniquely
        #If both sides played a card it will not be considered for this game
        myCardsSet = set(myCards)
        oppCardsSet = set(oppCards)

        myUniqueCards = myCardsSet.difference(oppCardsSet)
        oppUniqueCards = oppCardsSet.difference(myCardsSet)
        updateCardWinrate(myUniqueCards, win, cardsData)
        updateCardWinrate(oppUniqueCards, not win, cardsData)

    for cardId in cardsData:
        card = cardsData.get(cardId)
        winCount = card.get("winCount")
        gameCount = card.get("gameCount")
        if winCount and gameCount:
            card["winRate"] = float(winCount)/float(gameCount)
        else:
            card["winRate"] = -1
        cardsData[cardId] = card
        cardsDb.update_one({"_id": cardId}, {"$set": card})

    for game in gamesList:
        if game.get("result") == "win":
            win = True
        else:
            win = False
        myClass = game.get("hero")
        oppClass = game.get("opponent")
        myCards = []
        oppCards = []
        for cardObj in game.get("card_history"):
            player = cardObj.get("player")
            cardId = cardObj.get("card")
            card = cardsData.get(cardId)
            cardClass = card.get("cardClass")
            if player == "me":
                if cardClass == myClass or cardClass == "Neutral":
                    myCards.append(card)
            else:
                if cardClass == oppClass or cardClass == "Neutral":
                    oppCards.append(card)

        myUniqueCards = uniqueCardsFromList(myCards)
        oppUniqueCards = uniqueCardsFromList(oppCards)
        myUniqueCards.sort(key=lambda x: x.get("vertexId"), reverse=True)
        oppUniqueCards.sort(key=lambda x: x.get("vertexId"), reverse=True)
        updateEdgeWinrateFromCards(myUniqueCards, win, edgesData)
        updateEdgeWinrateFromCards(oppUniqueCards, not win, edgesData)

    for edgeName in edgesData:
        edge = edgesData[edgeName]
        winCount = edge.get("winCount")
        gameCount = edge.get("gameCount")
        if winCount and gameCount:
            edge["winRate"] = float(winCount) / float(gameCount)
        else:
            edge["winRate"] = -1
        edgeId = edge.get("_id")
        edgesDb.update_one({"_id": edgeId}, {"$set": edge})

############################## HELPER FUNCTIONS ####################################
def updateCardWinrate(cardList, win, cardsData):
    for cardId in cardList:
        card = cardsData.get(cardId)
        #Update gameCount
        if "gameCount" in card:
            card["gameCount"] += 1
        else:
            card["gameCount"] = long(1)
        #If win is true, update winCount
        if win:
            if "winCount" in card:
                card["winCount"] += 1
            else:
                card["winCount"] = long(1)
        cardsData[cardId] = card


def updateEdgeWinrateFromCards(cards, win, edgesData):
    for i in range(0, len(cards)):
        for j in range(i + 1, len(cards)):
            edge = {}
            vertexA = cards[i]
            vertexB = cards[j]
            if vertexA != vertexB:
                edgeName = str(vertexA.get("vertexId")) + "_" + str(vertexB.get("vertexId"))
                edge = edgesData[edgeName]
                if "gameCount" in edge:
                    edge["gameCount"] += 1
                else:
                    edge["gameCount"] = 1
                if win:
                    if "winCount" in edge:
                        edge["winCount"] += 1
                    else:
                        edge["winCount"] = 1
                edgesData[edgeName] = edge

def uniqueCardsFromList(cards):
    uniqueCards = []
    for card in cards:
        if not card in uniqueCards:
            uniqueCards.append(card)
    return uniqueCards

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()