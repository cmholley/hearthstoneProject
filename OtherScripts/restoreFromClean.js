var dbclean = connect('127.0.0.1:27017/hearthstoneClean');
var db = connect('127.0.0.1:27017/hearthstoneProject');

db.dropDatabase()

dbclean.copyDatabase("hearthstoneClean","hearthstoneProject");