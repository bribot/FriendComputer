import discord
from discord.ext import commands 
from discord import app_commands
from typing import Literal
import asyncio
import random as rand
from responses import *
import credentials
import npc
import atexit
# from computerConf import *
import time
import dnd5Gen as gen
import logging
import randomTables
import diceBag
import sqlite3 as sql
import duelSimulation as duel

import os
#from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

con = sql.connect("friendcomputer.db")
cur = con.cursor()

UV = ''' Amiga Computadora esta aqui para ayudarte

                                                                                
                                                                                
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░▒██████████████████████░░░░░░░░░
░░░░░░░░████████████████████████░░░░░░░░
░░░░░░░███████▓▒▒░░░░░░░▒▒▓█████▓░░░░░░░
░░░░░░█████▓░░░░░░░░░░░░░░░░▒▓███▓░░░░░░
░░░░░▓███▒░░░░░░░░░░░░░░░░░░░░░▓██▒░░░░░
░░░░▓███░░░░░░░▒▓█████▒░░░░░░░░░▓██▒░░░░
░░░▓███▒░░░░░░▓██████▒░░░░░░░░░░░▓██▒░░░
░░▒███▓░░░░░░████████▒░░░░░░░░░░░░███▒░░
░▒████▒░░░░░▒█████████▓▒░░▒▒░░░░░░████░░
'''

clearanceLvl = ["Infrared","Red","Orange","Yellow","Green","Blue","Indigo","Violet","Ultraviolet"]
clearanceScore = {"Infrared":0,
             "Red": 5000,
             "Orange": 8000,
             "Yellow": 13000,
             "Green": 21000,
             "Blue": 34000,
             "Indigo": 55000,
             "Violet": 89000,
             "Ultraviolet": 1337000000}
PCstats = {
        "id": 0,
        "name": 1,
        "infractions": 2,
        "clones": 3,
        "points": 4,
        "level": 5,
        "mutant": 6
    }
vat = npc.generator(stats=npc.rpg.NORTEStats)
banC = [] #['artificer','mystic (ua)','ranger (revised)']
banR = [] #['aarakocra','aasimar (fallen)','aasimar (scourge)','bugbear','dwarf (duergar)','elf (eladrin)','firbolg','genasi (air)','genasi (earth)','genasi (fire)','genasi (water)','gnome (deep)','gnome (rock)','goliath','half-elf (aquatic elf descent)','half-elf (drow descent)','half-elf (moon elf or sun elf descent)','half-elf (wood elf descent)','halfling (ghostwise)','halfling (stout)','hobgoblin','kenku','kobold','lizardfolk','shifter (razorclaw)','shifter (wildhunt)','triton','yuan-ti pureblood']
banb = [] #['cormanthor refugee','caravan specialist','city watch','clan crafter','cloistered scholar','cormanthor','refugee','courtier','earthspur miner','faction agent','far traveler','gate urchin','harborfolk','haunted one','hillsfar merchant','hillsfar smuggler','inheritor','investigator','knight of the order','mercenary veteran','mulmaster aristocrat','phlan refugee','secret identity','shade fanatic','trade sherrif','urban bounty hunter','uthgardt tribe member','waterdhavian noble']
vatXP = gen.generator(banclasses = banC, banraces = banR,banbg = banb)
convos=[]
LOG_FILENAME = time.ctime()+'.log'
# logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#client.Game("Paranoia")
#clones={"DM":0}
#infractions={"DM":0}
maxInfractions=3

tree = app_commands.CommandTree(client)

guild_id = 337628077775519744

@tree.command(
    name="r",
    description="roll some dice",
    #guild=discord.Object(guild_id)
)
async def rollDice(interaction, message: str):
    m = ""
    if "!" in message:
        m = "Operacion no soportada aun!"
    elif "d0" in message:
        m = "No hagas eso!"
    else:
        d = diceBag.rollDice(message)
        #m += "Esta modulo esta en beta!!!\n"
        m += "Rolling: " + message +"\n"
        m += "Dice: " + str(d[1])+"\n"
        m += "Result: " + str(d[0])
    await interaction.response.send_message(m)

@tree.command(
    name="races",
    description="Available races",
    #guild=discord.Object(guild_id)
)
async def races(interaction):
    m = ""
    for r in vatXP.races:
        m += r +"\n"
    await interaction.response.send_message(m)
    return

@tree.command(
    name="clases",
    description="Available clases",
    #guild=discord.Object(guild_id)
)
async def clases(interaction):
    m = ""
    for r in vatXP.classes:
        m += r +"\n"
    await interaction.response.send_message(m)

@tree.command(
    name="backgrounds",
    description="Available backgrounds",
    #guild=discord.Object(guild_id)
)
async def backgrounds(interaction):
    m = ""
    for r in vatXP.backgrounds:
        m += r +"\n"
    await interaction.response.send_message(m)

@tree.command(
    name="create",
    description='''Create a Caracter
    class, race, background''',
    #guild=discord.Object(guild_id)
)
async def createCharacter(interaction, message: str):
    m = "" 
    m = vatXP.interface(message)
#        print(m)
    if m == "error":
        logging.debug("----------------------------HERE------------------------------")
        logging.debug(message.content)
        await interaction.response.send_message(errorMessage())
    else:
        await interaction.response.send_message(m)

@tree.command(
    name="tabla",
    description="Available tables: |"+randomTables.tableIndex(),
    #guild=discord.Object(guild_id)
)
async def rollTable(interaction, message: str):
    s=message.lower()
    if len(s.split(' '))>1:
        await interaction.response.send_message("Solo puedes tirar en una tabla a la vez!")
        return
    name=s
    # if name == "rumores":
    #     await interaction.user.dm_channel.send("hewwo")
    # else:
    await interaction.response.send_message(randomTables.rollTable(name))

@tree.command(
    name="solostats",
    description= "Just stats for a new npc character"
)
async def justStats(interaction, message: str):
    s=message.lower()
    breed=s
    if breed=="raza":
        await interaction.response.send_message("Creando raza aleatoria...\n" +vat.randomTable())
        return
    for kind in npc.rpg.npcType:
        if breed==kind or breed=="npc":
            #await interaction.response.send_message("Generando clon")
            statsMessage = "Generando clon \n"
            if breed == "npc":
                breed="none"
            vat.generate(breed)
            statsMessage+="Los dados fueron:\n"   
            for s in vat.usedRolls:
                statsMessage+=str(s)+"\n"
            statsMessage+="Aqui esta tu clon\n"
            for s in vat.stats:
                statsMessage+=s+": "+str(vat.stats[s])+"\n"
            await interaction.response.send_message(statsMessage)
            #tmp = await message.channel.send("Tiene %d gp" % vat.money)
            return
    await interaction.response.send_message("No tengo registrado este tipo de clon en mi base de datos")
    return

@tree.command(
        name="my_stats", 
        description="Check stats"
)
async def checkPCstats(interaction):
    pc = interaction.user
    currentPc = getPCstats(pc)
    message = "----------------------- \n" \
    "Ciudadano %s \n" \
    "Infracciones: %d \n" \
    "Clones: %d \n" \
    "Puntos: %d \n" \
    "Nivel: %s \n" \
    "-----------------------" % (currentPc[PCstats["name"]],currentPc[PCstats["infractions"]],currentPc[PCstats["clones"]],currentPc[PCstats["points"]],clearanceLvl[currentPc[PCstats["level"]]])
    # print(message)
    await interaction.response.send_message(message)
    return

@tree.command(
        name="multipass",
        description="test function"
)
async def multipass(interaction,message: str):
    # awardPoints(interaction.user)
    return
@tree.command(name = "explica_duelo"
              , description = "Explica como funciona el sistema de duelo"
              )
async def explica_duelo(interaction):
    await interaction.response.send_message(duel.attackExplanation(),file=discord.File("./images/triangle.jpg"))
    return

#-----------------------------------------------------------------------------------------------
@tree.command(
        name="atacar", 
        description="Reta a un ciudadano a un duelo apostando puntos"
        )
async def atacar(interaction: discord.Interaction, ciudadano: discord.Member, attack: duel.attackLiteral, apuesta: int):
    pc = interaction.user
    msg0 = ""
    # print(interaction.id)
    if ciudadano.bot:
        return await interaction.response.send_message("No puedes atacar a un bot!")
    if ciudadano == pc:
        return await interaction.response.send_message("No puedes atacarte a ti mismo!")
    
    pc_current_points = getPCstats(pc)[PCstats["points"]]
    if pc_current_points == 0:
        apuesta = 100
        msg0 = "No tienes puntos para apostar. La apuesta se ha reducido a **100 puntos** de cortesia.\n"
    elif pc_current_points < apuesta:
        apuesta = pc_current_points
        msg0 = f"No tienes suficientes puntos para apostar esa cantidad. La apuesta se ha reducido a **{apuesta} puntos**.\n"

    # is this duel already happening?
    if any((d['citizen_member'].id == ciudadano.id and d['attacker_member'].id == pc.id) for d in duel.activeDuels.values()):
        return await interaction.response.send_message(f"**{ciudadano.display_name}** ya tiene un duelo pendiente. ¡Espera tu turno!", ephemeral=True)

    await interaction.response.send_message(f"{msg0}{pc.mention} ha retado a {ciudadano.mention} a un **duelo** apostando **{apuesta}** puntos! \n" 
                                            f"Usa la opcion de Reply en este mensaje con el nombre de tu arma para defenderte: \n`{', '.join(duel.attacks.keys())}`")
    message = await interaction.original_response()

    # SAVE DUEL DATA
    duel.activeDuels[message.id] = {
        "citizen_member": ciudadano,
        "attacker_member": pc,
        "initial_attack": attack,
        "original_channel": interaction.channel_id,
        "bet": apuesta
    }
    
@tree.command(
        name="duelos_activos",
        description="Muestra los duelos activos"
)
async def duelos_activos(interaction):
    if not duel.activeDuels:
        await interaction.response.send_message("No hay duelos activos en este momento.")
        return
    
    message = "**Duelos Activos:**\n"
    for duel_id, data in duel.activeDuels.items():
        message += f"- {data['attacker_member'].display_name} vs {data['citizen_member'].display_name} (Apuesta: {data['bet']} puntos)\n"
    
    await interaction.response.send_message(message)

@tree.command(name="cancelar_duelo", 
              description="Cancela duelos activos en los que estés involucrado"
              )
async def cancelar_duelo(interaction):
    pc = interaction.user
    duel_to_cancel = None
    
    for duel_id, data in duel.activeDuels.items():
        if data['citizen_member'].id == pc.id or data['attacker_member'].id == pc.id:
            duel_to_cancel = duel_id
            break
    
    if duel_to_cancel:
        del duel.activeDuels[duel_to_cancel]
        message = f"El duelo entre {data['attacker_member'].display_name} y {data['citizen_member'].display_name} ha sido cancelado. \n"
        message += f"{discountPoints(pc, data['bet'])} por tu **cobardia**!\n"
        await interaction.response.send_message(message)
    else:
        await interaction.response.send_message("No tienes duelos activos para cancelar.")

@tree.command(name="duelo_contra_bot",
                description="Reta a un duelo contra un NPC controlado por la Amiga Computadora"
    )
async def duelo_contra_bot(interaction, attack: duel.attackLiteral, apuesta: int):
    pc = interaction.user
    msg = ""
    pc_points=getPCstats(pc)[PCstats["points"]]
    if pc_points == 0:
        apuesta = 100
        msg = "No tienes puntos para apostar. La apuesta se ha reducido a **100 puntos** de cortesia.\n"
    elif pc_points < apuesta:
        msg = f"No tienes suficientes puntos para apostar esa cantidad. La apuesta se ha reducido a **{apuesta} puntos**.\n"
        apuesta = pc_points
    
    result, narration = duel.playSimulation_singleplayer(pc.display_name.capitalize(), attack)
    if result == 1:
        point_msg = awardPoints(pc, apuesta)
    elif result == 2:
        point_msg = discountPoints(pc, apuesta)
    else:
        point_msg = "Nadie gana ni pierde puntos."
    await interaction.response.send_message(
        f"{msg}\n*{narration}*\n{point_msg}")
        


@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    
    for i in client.guilds:
        logging.info(i)
#    print('------')
    await client.change_presence(activity=discord.Game(name="Paranoia"))

@client.event
async def on_message(message):
        
    if message.author.id == client.user.id:
        return
    
    # ------------------------------Duel Sim--------------------------------------
    # Verificar si el mensaje es un reply del mensaje original y si el usuario tiene un duelo pendiente
    if message.reference is not None and message.reference.message_id in duel.activeDuels and message.author.id == duel.activeDuels[message.reference.message_id]["citizen_member"].id:
        eleccion = message.content.capitalize()
        
        if eleccion in duel.attacks.keys():  
            datos = duel.activeDuels.pop(message.reference.message_id) 
            result, narration = duel.playSimulation(datos["attacker_member"].name.capitalize(), message.author.name.capitalize(), datos["initial_attack"], eleccion)
            canal = client.get_channel(datos["original_channel"])
            if result == 1:
                point_msg = pointExchange(datos["attacker_member"], message.author, datos["bet"])
            elif result == 2:
                point_msg = pointExchange(message.author, datos["attacker_member"], datos["bet"])
            else:
                point_msg = "Nadie gana ni pierde puntos."
            if canal:
                await canal.send(
                    f"*{narration}*"
                    f"\n---\n"
                    f"**¡El duelo ha concluido!**\n"
                    f"{point_msg}"
                    
                )
        else:
            await message.author.send(f"❌ Arma no válida. Elige una de: {', '.join(duel.attacks.keys())}")
        await message.delete()
        msg = await message.channel.fetch_message(message.reference.message_id)
        await msg.delete()
        return    
    # --------------------------------------------------------------------------------
    
    if message.content.startswith("hewwo"):
        logging.info(message.guild)
        logging.info(message.channel)
        logging.info(message.author)
        logging.info(message.author.dm_channel)
        if message.author.dm_channel == None:
            await message.author.create_dm()
            logging.info(message.author.dm_channel)
        await message.author.dm_channel.send("hewwo")
        return

    # if message.content.startswith("test"):
    #     await message.channel.send("test")
    #     return
    if message.content.startswith("/sync") and message.author.name=="brib0t":
        await tree.sync()
        await message.channel.send("Commands Synced")
        return
    
    if message.content.startswith("Amiga computadora"):
        await message.channel.send("La Amiga computadora esta aqui para ayudarte")

#------------------------------------------------
    if "acusar" in message.content.lower():
        tmp = await message.channel.send(checkAcusation(message))
        return
        #print(message.mentions[0].discriminator)
        # pc1 = str(message.author)
        # if "Amiga Computadora" in str(message.mentions):
        #     tmp = await message.channel.send("Acusar a Amiga Computadora se considera un acto de traición!")
        #     # for i in range(3):
        #     #     tmp = await message.channel.send("{0.name} ".format(message.author) + kill(str(message.author)))
        #     #     time.sleep(2)
        #     return
        # for member in message.mentions:
        #     pc1 = message.author
        #     pc2 = member
        #     #tmp = await message.channel.send("Estas acusando a "+member.name)
        #     if rand.randint(0,100)>0:
        #         tmp = await message.channel.send("La Amiga Computadora ha considerado cierta tu acusación")
        #         pc=pc2
        #     else:
        #         tmp = await message.channel.send("Esta acusación es falsa y no sera tolerado el mentirle a la Amiga Computadora")
        #         pc=pc1
            
        #     tmp = await message.channel.send(pc.name+" "+ str(awardInfraction(pc,1)))
        # return
#----------------------------------------------
    for res in respond:
        if res in message.content.lower():
            tmp = await message.channel.send("{0.name} ".format(message.author)+respond[res].format(message.author))               
            #print(res+" {0.name}".format(message.author))
            #print(str(message.author))
            if respond[res].startswith(":warning:"):
                tmp = await message.channel.send("{0.name} ".format(message.author) + awardInfraction(message.author))
            return

    # if message.content.startswith("Ultravioleta"):
    #    if [n.name == "Admin" for n in message.author.roles]: #str(message.author.name) != "brib0t" or 
    #     await message.channel.send(UV) 
    #     tmp = await message.channel.send("------------------------\n Name:Infractions:Clones")
    #     # for m in clones:
    #     #     print(m + " : " + str(infractions[m])+" : "+str(clones[m]))
    #     #     tmp = await message.channel.send(m + " : " + str(infractions[m])+" : "+str(clones[m]))
    #     # tmp = await message.channel.send("------------------------")
    #     print("------------------------")

    #    return
            

def errorMessage():
    return "Algo salio mal, esto es tu culpa"

# def kill(pc):
#     return awardInfraction(pc,maxInfractions)

def pointUpdate(pc,points: int):
    currentPC = getPCstats(pc)
    currentPoints = currentPC[PCstats["points"]]
    currentLvl = currentPC[PCstats["level"]]
    pcPoints = currentPoints + points
    if pcPoints < 0:
        pcPoints=0
    updatePCStats(pc,"points",pcPoints)
    if currentLvl<8 & pcPoints >= clearanceScore[clearanceLvl[currentLvl+1]]:
        #TO DO: SEND USER A LVL UP MESSAGE
        print("lvl UP!")
        updatePCStats(pc,"level",currentLvl+1)
    if currentLvl > 0 & pcPoints <= clearanceScore[clearanceLvl[currentLvl-1]]:
        print("LVL Down")
    return

def isPCindb(pc):
    query = "SELECT name FROM citizens WHERE id = ?"
    res = cur.execute(query, (pc.id,))
    if res.fetchone() is None:
        query = "INSERT INTO citizens VALUES (?,?,?,?,?,?,?)"
        res = cur.execute(query, (pc.id,pc.name,0,0,500,0,"mutant"))
        con.commit()
        print("new user added")
    return

def getPCstats(pc):
    isPCindb(pc)
    query = "SELECT * FROM citizens WHERE id = ?"
    res = cur.execute(query,(pc.id,))
    return res.fetchone()

def updatePCStats(pc, pcStat = "points", statValue = 100):
    isPCindb(pc)
    query = f"UPDATE citizens SET {pcStat} = ? WHERE id = ?"
    res = cur.execute(query,(statValue,pc.id,))
    con.commit()
    return

def pointExchange(pc1, pc2, points):
    pc2_stats = getPCstats(pc2)
    if pc2_stats[PCstats["points"]]<points:
        points = pc2_stats[PCstats["points"]]
    pointUpdate(pc1,points)
    pointUpdate(pc2,-points)
    return pc1.mention + " ha ganado **%d puntos** de %s" % (points, pc2.mention)

def awardPoints(pc,points = 0):
    if points == 0:
        points = rand.randint(0,500)
    pointUpdate(pc,points)    
    message = "%s Has ganado **%d puntos**" % (pc.name, points)
    # print(message)
    return message
# Returns str message
def discountPoints(pc,points = 0):
    if points == 0:
        points = rand.randint(0,500)
    pointUpdate(pc,-points)    
    message = "%s Has perdido **%d puntos**" % (pc.name, points)
    # print(message)
    return message
#Returns message with infractions and points
def awardInfraction(pc,points = 0):
    # Get member stats
    currentPC = getPCstats(pc)
    # Get infractions
    currentInfractions = currentPC[PCstats["infractions"]]
    # Add infraction & update
    currentInfractions = currentInfractions+1
    updatePCStats(pc,"infractions",currentInfractions)
    # sub points

    if points == 0:
        points = rand.randint(0,300)
    pointUpdate(pc,-points)

    #TO DO: Check for infractions and CLones
    #check if new clone
    if (currentInfractions%maxInfractions)==0:
        currentClones = currentPC[PCstats["clones"]]+1
        updatePCStats(pc,"clones",currentClones)
        return death[rand.randint(0,len(death)-1)]+", "+live[rand.randint(0,len(live)-1)]+". Has matado a %d de tus clones y perdiste %d puntos" % (currentClones, points)
    else:
        return "%s tienes %d infraccion(es) y se te han descontado %d puntos" % (pc.name, currentInfractions, points) 

def checkAcusation(message):
    response = ""
    pc1 = message.author
    if "Amiga Computadora" in str(message.mentions):
        points = rand.randint(100, 1000)
        pointUpdate(pc1,points)
        response = response + "Acusar a Amiga Computadora se considera un acto de traición! \n Has perdido %d puntos" % points
        # print(message)
        # tmp = await message.channel.send(message)
        return response
    pc1_stats = getPCstats(pc1)
    for member in message.mentions:
        pc2 = member
        pc2_stats = getPCstats(pc2)
        pc1Power = rand.randint(0,(pc1_stats[PCstats["level"]]+1)*100)
        pc2Power = rand.randint(0,(pc2_stats[PCstats["level"]]+1)*100)
        points = abs(pc1Power - pc2Power) * 10
        if pc1Power>pc2Power:
            response = response + "La Amiga Computadora ha considerado cierta tu acusación contra %s. " % (pc2.name)
            response = response + awardPoints(pc1,points) + "\n"
            response = response + awardInfraction(pc2)
        else:
            response = "Tu acusación contra %s es falsa y no sera tolerado el mentirle a la Amiga Computadora! " % (pc2.name)
            response = response + awardPoints(pc2,points) + "\n"
            response = response + awardInfraction(pc1)
        
    return response

#bot.run(credentials.botToken)
client.run(credentials.botToken) 

