import constants
import os
import time
from pymongo import MongoClient

'''
This script prints a CSV file where every row is an edge in the edges collection
It provides the name of the edge, 
'''
def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards
    edgesDb = db.edges

    #Create card dictionary
    cardsList = list(cardsDb.find())
    cardsData = {}
    for card in cardsList:
        objectId = card.get("_id")
        cardsData[objectId] = card


    edgesList = list(edgesDb.find())

    with open(constants.WEIGHTS_CSV_FILE_LOCATION, 'wb') as file:
        file.write("edgeName, cardA, cardB, edgeClass, weight, gameCount, winCount, winRate\n")
        for edge in edgesList:
            if edge.get("edgeName") == "1005_202":
                a = 1
            cardAName = cardsData.get(edge.get("vertexAObjectId")).get("name")
            cardBName = cardsData.get(edge.get("vertexBObjectId")).get("name")

            cardAName = cardAName.replace(',','')
            cardBName = cardBName.replace(',','')

            line = str(edge.get("edgeName"))+","
            line += str(cardAName)+","
            line += str(cardBName)+","
            line += str(edge.get("edgeClass"))+","
            line += str(edge.get("weight"))+","
            line += str(edge.get("gameCount")) + ","
            line += str(edge.get("winCount")) + ","
            line += str(edge.get("winRate"))
            file.write(line)
            file.write("\n")

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()
