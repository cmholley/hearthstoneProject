import constants
import os
import json
import time
from pymongo import MongoClient



def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards
    edgesDb = db.edges

    #Create card dictionary
    cardsList = list(cardsDb.find({"gameCount": {"$gte": 1}}))
    cardsData = {}
    for card in cardsList:
        objectId = card.get("_id")
        cardsData[objectId] = card


    edgesList = list(edgesDb.find().sort("weight",-1).limit(constants.MAX_EDGES_IN_VIS))
    maxGameCount = cardsDb.find_one(sort=[("gameCount", -1)]).get("gameCount")

    #We will use a dictionary to allow constant time checks if the card has already been added to the nodes list
    addedCards = {}

    graphJson = {}
    graphJson["directed"] = False
    graphJson["multiGraph"] = False
    graphJson["graph"] = {}
    graphJson["nodes"] = []
    graphJson["links"] = []




    for edge in edgesList:
        link = {}
        cardA = cardsData.get(edge.get("vertexAObjectId"))
        cardB = cardsData.get(edge.get("vertexBObjectId"))

        #Check if card is in nodes list already
        if cardA.get("id") not in addedCards:
            addedCards[cardA.get("id")] = True
            graphJson["nodes"].append(nodeFromCard(cardA, maxGameCount))
        if cardB.get("id") not in addedCards:
            addedCards[cardB.get("id")] = True
            graphJson["nodes"].append(nodeFromCard(cardB, maxGameCount))

        link["source"] = cardA.get("name")
        link["target"] = cardB.get("name")
        graphJson["links"].append(link)

    with open(constants.GRAPH_JSON_FILE_LOCATION, 'wb') as outfile:
        json.dump(graphJson,outfile)


def nodeFromCard(card, maxGameCount):
    '''
        Colors
        Light Blue -- Mage (#69CCF0)
        Blue -- Shaman (#0070DE)
        White -- Priest (#FFFFFF)
        Tan -- Warrior (#C79C6E)
        Green -- Hunter (#ABD473)
        Light Yellow -- Rogue (#FFF569)
        Pink -- Paladin (#F58CBA)
        Purple -- Warlock (#9482C9)
        Orange -- Druid (#FF7D0A)
    '''

    classColors = {
        "Mage": "rgb(105,204,240)",
        "Shaman": "rgb(0,112,222)",
        "Priest": "rgb(255,255,255)",
        "Warrior": "rgb(199,156,110)",
        "Hunter": "rgb(171,212,115)",
        "Rogue": "rgb(255,245,105)",
        "Paladin": "rgb(245,140,186)",
        "Warlock": "rgb(148,130,201)",
        "Druid": "rgb(255,125,10)"
    }

    node = {}
    node["radius"] = (32 / float(maxGameCount)) * (card.get("gameCount")) + 3
    node["class"] = card.get("cardClass")
    node["color"] = classColors.get(card.get("cardClass"))
    node["id"] = card.get("name")
    node["desc"] = "Name: " + card.get("name") + ", Class: " + card.get("cardClass")
    return node

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()