var dbclean = connect('127.0.0.1:27017/hearthstonePreWinRate');
var db = connect('127.0.0.1:27017/hearthstoneProject');

db.dropDatabase()

dbclean.copyDatabase("hearthstonePreWinRate","hearthstoneProject");