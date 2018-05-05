# hearthstoneProject
This project was completed during the Spring 2018 semester in order to receive honors credit for MATH 4315 Graph Theory and Applications taught by Dr. Josic

# Getting started
In order to generate results for yourself, pull the repository down and follow these steps: 

* Import the .json files from the data/partitions folder into a MongoDb database. The default name for the database is hearthstoneProject. The default collection is named games. 
* Load OtherScripts/rankedGames.json in the Mongo shell to create the rankedGames collection.
* Create a constants.py using the pattern below
* Set printFilesBool in PythonScripts\fullRun.py to true and run fullRun.py

## constants.py
```python
CARDS_JSON_LOCATION = "{location for cards json, default is in data/cards.json}"

#Change if your mongo instance isn't local
DBHOST = "localhost"
DBPORT = 27017

EDGES_CSV_FILE_LOCATION = "{location for edges csv}"
GRAPH_JSON_FILE_LOCATION = "{location for graph.json for visualization}"
CARDS_CSV_FILE_LOCATION = "{location for cards csv}"

MAX_EDGES_IN_VIS = 5000
```

# Visualization
This visualization portion of this project can be found in a separate repository [here](https://github.com/cmholley/hsCardGraph). The graph.json file from that repository is generated by the writeGraphJson.py script.
