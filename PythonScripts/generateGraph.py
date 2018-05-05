import constants
import os
import time
from pymongo import MongoClient

'''
This function will generate the edges of the graphs. The weight of each edge represents the number of times
the two connected cards were played together. If one of the cards is not neutral, the weight is multplied by the
class multiplier to compensate for the limited space of games. Edges will be labeled <vertexAId>_<vertxBId> where
vertexA is the vertex with the higher vertex id
'''
#Declare outside of run so other functions can access it

def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards
    gamesDb = db.rankedGames
    edgesDb = db.edges

    gamesList = list(gamesDb.find())
    cardsList = list(cardsDb.find())

    edgeData = {}
    cardsData = {}
    edgeData = {}

    # Create card dictionary

    for card in cardsList:
        objectId = card.get("_id")
        cardsData[objectId] = card

    '''
    NOTE: After further investigation, these weight rules were deemed unneccessary. The reality of how the game is played
    does not match the assumptions below. More detail on this decision is included in the paper. This section has been
    commented out rather then removed so that others may use these multipliers if deemed necessary

    To make the weights of the graph comparable, we have to account for unique cards. Because these cards can 
    only be played by one class, they will be less common regardless of how powerful they are. So, we use a multiplier
    for each class, which is the inverse of the portion of all players in the set who played that class. Ideally this 
    would be 1/9 for each class, but the data does not follow that breakdown, so we use the experimental percentages from
    the dataset

    totalGames = 0
    classCounters = {
        "Druid": 0,
        "Hunter": 0,
        "Mage": 0,
        "Paladin": 0,
        "Priest": 0,
        "Rogue": 0,
        "Shaman": 0,
        "Warlock": 0,
        "Warrior": 0,
    }
    classPercentages = {}
    classMultipliers = {"Neutral": 1}
    for game in gamesList:
        totalGames += 1
        myClass = game.get("hero")
        oppClass = game.get("opponent")
        classCounters[myClass] += 1
        classCounters[oppClass] += 1

    for key in classCounters:
        count = float(classCounters[key])
        #We are seeing how many players played each class. Each game has two players, so totalGames*2
        percentage = count/(totalGames*2)
        classPercentages[key] = percentage

    for key in classPercentages:
        mult = 1/classPercentages.get(key)
        classMultipliers[key] = mult

    '''

    for game in gamesList:
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

        myCards.sort(key=lambda x: x.get("vertexId"), reverse=True)
        oppCards.sort(key=lambda x: x.get("vertexId"), reverse=True)
        generateEdgesFromCardList(myCards, edgeData)
        generateEdgesFromCardList(oppCards,edgeData)


    for key in edgeData:
        edge = edgeData[key]
        edgesDb.insert(edge)

def generateEdgesFromCardList(cards, edgeData):
    for i in range(0,len(cards)):
        for j in range(i+1,len(cards)):
            edge = {}
            vertexA = cards[i]
            vertexB = cards[j]
            edgeClass = "Neutral"
            if vertexA.get("cardClass") != "Neutral":
                edgeClass = vertexA.get("cardClass")
            if vertexB.get("cardClass") != "Neutral":
                edgeClass = vertexB.get("cardClass")

            if vertexA != vertexB:
                edgeName = str(vertexA.get("vertexId")) + "_" + str(vertexB.get("vertexId"))
                if (edgeName not in edgeData):
                    vertexAObjectId = vertexA.get("_id")
                    vertexBObjectId = vertexB.get("_id")
                    edge["vertexAObjectId"] = vertexAObjectId
                    edge["vertexBObjectId"] = vertexBObjectId
                    edge["edgeName"] = edgeName
                    edge["weight"] = 1
                    edge["edgeClass"] = edgeClass
                    edgeData[edgeName] = edge
                else:
                    edge = edgeData[edgeName]
                    edge["weight"] += 1
                    edgeData[edgeName] = edge

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()