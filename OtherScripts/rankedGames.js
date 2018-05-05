var db = connect('127.0.0.1:27017/hearthstoneProject');

db.games.find({mode:"ranked"}).forEach(function(doc){
   db.rankedGames.insert(doc);
});