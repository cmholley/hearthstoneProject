import constants
from pymongo import MongoClient

'''
This is for quick scratch work and investigation. 
'''

client = MongoClient(constants.DBHOST, constants.DBPORT)

# Get the hearthstoneProject database
db = client.hearthstoneProject
cardsDb = db.cards
gamesDb = db.rankedGames

heroCardList = []
typeList = []
gamesData = list(gamesDb.find())
#Create card dictionary
cardsList = list(cardsDb.find())
cardsData = {}
for card in cardsList:
    type = card.get("type")
    if type == "HERO":
       heroCardList.append(card)

myList = [1,1,2,3,4]
print myList
myList = list(set(myList))

print myList


'''
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
for game in gamesData:
    totalGames += 1
    myClass = game.get("hero")
    classCounters[myClass] += 1

for key in classCounters:
    count = float(classCounters[key])
    percentage = count/totalGames
    classPercentages[key] = percentage
print totalGames
print classPercentages
'''