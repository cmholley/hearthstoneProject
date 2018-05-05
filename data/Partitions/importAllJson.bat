@echo off
for %%f in (*.json) do (
    "mongoimport.exe" --jsonArray --db hearthstoneProject --collection games --file %%~nf.json
)