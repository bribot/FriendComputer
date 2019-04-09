# RPG Reference


# Primer numero es favorecedor en posición y segundo es modificador
# 0 significa no favorecedor
# TODO Remake the class system 

adalid=[[1,0],[2,0],[0,0],[0,0],[0,0],[3,0]]
ranger=[[2,0],[1,0],[3,0],[0,0],[4,0],[0,0]]
none=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
villager=[[0,-2],[0,-2],[0,-2],[0,-2],[0,-2],[0,-2]]
wizard=[[6,0],[0,0],[0,0],[1,0],[0,0],[0,0]]
barbarian=[[1,0],[3,0],[2,0],[0,0],[4,0],[0,0]]
rogue=[[0,0],[1,0],[0,0],[0,0],[0,0],[0,0]]
bard=[[0,0],[2,0],[0,0],[3,0],[0,0],[1,0]]
sorcerer=[[0,0],[0,0],[0,0],[2,0],[0,0],[1,0]]
fighter=[[1,0],[2,0],[3,0],[0,0],[0,0],[0,0]]
druid=[[0,0],[2,0],[2,0],[0,0],[1,0],[2,0]]
paladin=[[0,0],[6,0],[0,0],[5,0],[0,0],[1,0]]
monk=[[0,0],[0,0],[0,0],[5,0],[1,0],[6,0]]

alquimist=[[0,0],[2,0],[0,0],[1,0],[0,0],[0,0]]
artificier=[[1,0],[0,0],[0,0],[1,0],[0,0],[2,0]]
summoner=[[0,0],[0,0],[0,0],[2,0],[0,0],[1,0]]
witch=[[0,0],[0,0],[0,0],[1,0],[0,0],[2,0]]
cleric=[[0,0],[0,0],[0,0],[3,0],[1,0],[2,0]]
inquisitor=[[0,0],[0,0],[0,0],[0,0],[1,0],[0,0]]
magus=[[2,0],[0,0],[0,0],[1,0],[0,0],[0,0]]

cat=[[0,0],[1,0],[0,0],[2,0],[3,0],[0,0]]

NORTERaces={
        "1-20":"humano (cardo)",
        "21-35":"humano (rakibi)",
        "36-40":"humano (ocitano)",
        "41-55":"enano (eskero)",
        "56-65":"elfo (norno)",
        "66-75":"halfling",
        "76-85":"gnomos",
        "86-95":"elfo (sitha)",
        "99-100":"changeling"
        }
randomTables={
        "races":NORTERaces
        }

NORTEMoney={
        "very high":"5d6*10",
        "high":"4d6*10",
        "medium":"3d6*10",
        "low":"2d6*10",
        "very low":"1d6*10"
        }

npcType={
        "none":[none,"medium"],
        "aldeano":[villager,"very low"],
        "adalid":[adalid,"very high"],
        "alquimista":[alquimist,"medium"],
        "mago":[wizard,"low"],
        "magus":[magus,"high"],
        "barbaro":[barbarian,"medium"],
        "bruja":[witch,"medium"],
        "clerigo":[cleric,"high"],
        "ladron":[rogue,"high"],
        "bardo":[bard,"medium"],
        "hechicero":[sorcerer,"low"],
        "inquisidor":[inquisitor,"high"],
        "invocador":[summoner,"low"],
        "guerrero":[fighter,"very high"],
        "druida":[druid,"low"],
        "ranger":[ranger,"very high"],
        "paladin":[paladin,"very high"],
        "monje":[monk,"very low"],
        "gato":[cat,"very high"]
        }

DNDStats={
        "STR":0,
        "DEX":0,
        "CON":0,
        "INT":0,
        "WIS":0,
        "CHA":0
        }

NORTEStats={
        "Fue":0,
        "Dex":0,
        "Con":0,
        "Int":0,
        "Sab":0,
        "Car":0
        }
CoCStats={
        "STR":0,
        "DEX":0,
        "POW":0,
        "CON":0,
        "APP":0,
        "EDU":0,
        "SIZ":0,
        "INT":0
        }
TOYStats={
        "Voluntad":0,
        "Cognicion":0,
        "Versatilidad":0,
        "Intensidad":0
        }
