var db = connect('127.0.0.1:27017/hearthstoneProject');

db.copyDatabase("hearthstoneProject","hearthstoneClean");