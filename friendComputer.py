import discord
from discord.ext import commands 
from discord import app_commands
import asyncio
import random as rand
from responses import *
import credentials
import npc
import atexit
from computerConf import *
import time
import dnd5Gen as gen
import logging
import randomTables
import diceBag

import os
#from openai import OpenAI




# TODO: USE BOT API
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



description = ''' Amiga Computadora esta aqui para ayudarte

                                                                                
                                                                                
                 .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  
                /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                
               (@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.               
              (@@@@@@@@@@@@@@@@@%*.            ,#&@@@@@@@@@@@@@@@*              
             /@@@@@@@@@@@@@*                         .&@@@@@@@@@@@(             
            %@@@@@@@@@@#                                 ,@@@@@@@@@/            
           &@@@@@@@@#                                       *@@@@@@@#           
          @@@@@@@@/                                           ,@@@@@@#          
        .@@@@@@@%                .%@@@@@@@@@@@#                 (@@@@@&         
       ,@@@@@@@/              %@@@@@@@@@@@@@.                    .@@@@@@        
      ,@@@@@@@/             @@@@@@@@@@@@@@@                       .@@@@@@       
     *@@@@@@@%            *@@@@@@@@@@@@@@@%                        /@@@@@@      
    /@@@@@@@@.           *@@@@@@@@@@@@@@@@@.                        @@@@@@@,    
   (@@@@@@@@@            &@@@@@@@@@@@@@@@@@@&          #.           %@@@@@@@,   
  /@@@@@@@@@@            @@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@*           %@@@@@@@@/  
 (@@@@@@@@@@@.           %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.           &@@@@@@@@@#'''



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

def turningOff():
    f = open("computerConf.py","w+")
    f.write("clones=")
    f.write(str(clones))
    f.write("\n")
    f.write("infractions=")
    f.write(str(infractions))
    atexit.register(turningOff)

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
        tmp = await message.channel.send("La Amiga computadora esta aqui para ayudarte")

#------------------------------------------------
    if "!acusar" in message.content:
        #print(message.mentions[0].discriminator)
        pc1 = str(message.author)
        if "Amiga Computadora" in str(message.mentions):
            tmp = await message.channel.send("Acusar a Amiga Computadora se considera un acto de traición!")
            for i in range(3):
                tmp = await message.channel.send("{0.name} ".format(message.author) + kill(str(message.author)))
                time.sleep(2)
            return


        for member in message.mentions:
            pc2 = member.name+"#"+member.discriminator
            #tmp = await message.channel.send("Estas acusando a "+member.name)
            if rand.randint(0,100)>50:
                tmp = await message.channel.send("La Amiga Computadora ha considerado cierta tu acusación")
                pc=pc2
            else:
                tmp = await message.channel.send("Esta acusación es falsa y no sera tolerado el mentirle a la Amiga Computadora")
                pc=pc1
            
            tmp = await message.channel.send(pc+" "+ awardInfraction(pc,1))
        return
#----------------------------------------------
    if message.content.startswith("!kill"):
        pc1 = str(message.author)
        #print(pc1)
        #print(str(message.mentions))
        
        if pc1.split("#")[0] in str(message.mentions):
            tmp = await message.channel.send("{0.name}".format(message.author)+" La felicidad es mandatoria y el asesinato propio no es permitido. Toma una pildora de la felicidad :pill:")
            return
        if "Amiga Computadora" in str(message.mentions):
            tmp = await message.channel.send("Tratar de matar a Amiga Computadora se considera un acto de traición!")
            for i in range(5):
                tmp = await message.channel.send("{0.name} ".format(message.author) + kill(str(message.author)))
                time.sleep(2)
            return
        for member in message.mentions:
            pc2 = member.name+"#"+member.discriminator
            if rand.randint(0,100)>80:
                tmp = await message.channel.send("La Amiga Computadora ha considerado cierta tu acusación")
                pc=pc2
            else:
                tmp = await message.channel.send("Esta acusación es falsa y no sera tolerado el mentirle a la Amiga Computadora")
                pc=pc1
            
            tmp = await message.channel.send(pc+" "+ kill(pc))
        return
#-----------------------------------------------------------------------------------
    if "campal" in message.content.lower():
        tmp = await message.channel.send("Todos saben que Alito fue a Campal")



# #-----------------------------------------------
    

#-----------------------------------------------
# FORBIDDEN!!!
#-----------------------------------------------
    if "abys" in message.content.lower():
        tmp = await message.channel.send("Conocer la palabra Abyss es un acto de traicion!")
        tmp = await message.channel.send("{0.name} ".format(message.author) + awardInfraction(str(message.author),1))

    if "walker" in message.content.lower():
        tmp = await message.channel.send("Conocer la palabra walker es un acto de traicion!")
        tmp = await message.channel.send("{0.name} ".format(message.author) + awardInfraction(str(message.author),1))

    if "pastel" in message.content.lower():
        tmp = await message.channel.send("Conocer la palabra pastel es un acto de traicion!")
        tmp = await message.channel.send("{0.name} ".format(message.author) + awardInfraction(str(message.author),1))
        
    if message.content.startswith("Ultravioleta"):
       if str(message.author.name) != "brib0t":
           return
       print("------------------------")
       print("Name:Infractions:Clones")
       
       tmp = await message.channel.send("------------------------\n Name:Infractions:Clones")
       for m in clones:
           print(m + " : " + str(infractions[m])+" : "+str(clones[m]))
           tmp = await message.channel.send(m + " : " + str(infractions[m])+" : "+str(clones[m]))
       tmp = await message.channel.send("------------------------")
       print("------------------------")

       return
#-----------------------------------------------
    for res in respond:
        if res in message.content.lower():
            tmp = await message.channel.send("{0.name} ".format(message.author)+respond[res].format(message.author))               
            #print(res+" {0.name}".format(message.author))
            #print(str(message.author))
            if "regla" not in res:
                return
            tmp = await message.channel.send("{0.name} ".format(message.author) + awardInfraction(str(message.author),1))
            

def errorMessage():
    return "Algo salio mal, esto es tu culpa"

def kill(pc):
    return awardInfraction(pc,maxInfractions)

def awardInfraction(pc,n):
    if pc not in clones:
        clones[pc]=0
        infractions[pc]=0

    infractions[pc]+=n

    if infractions[pc]>=maxInfractions:
        clones[pc]+=1
        infractions[pc]=0
        return death[rand.randint(0,len(death)-1)]+", "+live[rand.randint(0,len(live)-1)]+" Tus infracciones regresan a 0, has matado a %d de tus clones" % clones[pc]
    else:
        return "tienes %d infraccion(es)" % infractions[pc]


#bot.run(credentials.botToken)
client.run(credentials.botToken) 

