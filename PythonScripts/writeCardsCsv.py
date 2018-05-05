import constants
import os
import time
from pymongo import MongoClient

'''
This script prints a CSV file where every row is an card in the cards collection
It provides all information about the card except for the object id 
'''
def run():
    client = MongoClient(constants.DBHOST, constants.DBPORT)

    # Get the hearthstoneProject database
    db = client.hearthstoneProject
    cardsDb = db.cards

    cardsList = list(cardsDb.find())


    #Create list of headers
    ignoredHeaders = ["_id","mechanics"]
    headerCard = cardsList[1]
    headerList = []
    for key in headerCard:
        if key not in ignoredHeaders:
            headerList.append(key)

    with open(constants.CARDS_CSV_FILE_LOCATION,'wb') as file:
        #Write headers
        headers = ""
        for i in range(0,len(headerList)-1):
            headers += headerList[i] + ","
        headers += headerList[len(headerList)-1]+"\n"
        file.write(headers)
        #Write data
        for card in cardsList:
            line = ""
            for i in range(0, len(headerList) - 1):
                key = headerList[i]
                line += str(card.get(key)) + ","
            key = headerList[len(headerList)-1]
            line += str(card.get(key)) + "\n"
            file.write(line)

def start():
    start = time.time()
    print "Running ", os.path.basename(__file__)
    run()
    end = time.time()
    print "Finished ", os.path.basename(__file__), " in ", (end-start), " seconds"

if __name__ == '__main__':
    start()