import discord
from discord.ext import commands 
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

# TODO: USE BOT API
client = discord.Client()
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


class convo():
    def __init__(self,author,message,onGoing):
        return    
    
    def getResponse():
        return "OwO"
        

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
#        print("------------------------")
        
# NEW GENERATOR
        
    if message.content.startswith("!razas"):
        m = ""
        for r in vatXP.races:
            m += r +"\n"
        tmp = await message.channel.send(m)
    
    if message.content.startswith("!clases"):
        m = ""
        for r in vatXP.classes:
            m += r +"\n"
        tmp = await message.channel.send(m)
        
    if message.content.startswith("!trasfondos"):
        m = ""
        for r in vatXP.backgrounds:
            m += r +"\n"
        tmp = await message.channel.send(m)
    
    if message.content.startswith("!crear "):
        m = ""     
        mess=message.content[7:]
        m = vatXP.interface(mess)
#        print(m)
        if m == "error":
            logging.debug("----------------------------HERE------------------------------")
            logging.debug(message.content)
            tmp = await message.channel.send(errorMessage())
        else:
            tmp = await message.channel.send(m)
            
# -------------------------------------------------
    if message.content.startswith("/r "):
        m = ""
        if '*' in message.content or "!" in message.content:
            m = "Operacion no soportada aun!"
        elif "d0" in message.content:
            m = "No hagas eso!"
        else:
            d = diceBag.rollDice(message.content[3:])
            m += "Esta modulo esta en beta!!!\n"
            m += "Roll: " + str(d[1])+"\n"
            m += "Resultado: " + str(d[0])
        tmp = await message.channel.send(m)
        return
        
#------------------------------------------------
    if message.content.startswith("!ayuda"):
        tmp = await message.channel.send(
            '''Lista de comandos de Amiga Computadora: 
            \n!acusar @nombre: Acusar a alguien de traicion con amiga computadora
            \n!kill @nombre: Intento de traicion a alguien
            \n!crear class, race, background: Crea un personaje utilizando la base de datos de 5e
            \n!razas: Muestra la lista de razas
            \n!clases: Muestra la lista de clases
            \n!trasfondos: Muestra la lista de trasfondos
            \n!soloStats clase: Crea los stats de una clase (deprecado)
            \n!tabla <nombre de la table>: Da un resultado aleatorio de una tabla guardada
            '''
            )
        return
#------------------------------------------------
    if message.content.startswith("!tabla "):
        s=message.content.lower()
        if len(s.split(' '))>2:
            tmp = await message.channel.send("Solo puedes tirar en una tabla a la vez!")
            return
        elif len(s.split(' ')) == 1:
            tmp = await message.channel.send("Necesitas darme una tabla, cerebro de soylent")
            return
        command,name=s.split(" ")
        if name == "rumores":
            
            tmp = await message.author.send(randomTables.rollTable(name))
        else:
            tmp = await message.channel.send(randomTables.rollTable(name))
        
#------------------------------------------------
#------------------------------------------------
    if message.content.startswith("!soloStats "):
        s=message.content.lower()
        command,breed=s.split(" ")
        if breed=="raza":
            tmp = await message.channel.send("Creando raza aleatoria...\n" +vat.randomTable())
            return
        for kind in npc.rpg.npcType:
            if breed==kind or breed=="npc":
                tmp = await message.channel.send("Generando clon")
                if breed == "npc":
                    breed="none"
                vat.generate(breed)
                statsMessage="Los dados fueron:\n"   
                for s in vat.usedRolls:
                    statsMessage+=str(s)+"\n"
                statsMessage+="Aqui esta tu clon\n"
                for s in vat.stats:
                    statsMessage+=s+": "+str(vat.stats[s])+"\n"
                tmp = await message.channel.send(statsMessage)
                #tmp = await message.channel.send("Tiene %d gp" % vat.money)
                return
        tmp = await message.channel.send("No tengo registrado este tipo de clon en mi base de datos")
        return
        

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



#-----------------------------------------------
    if message.content.startswith("Amiga computadora"):
        tmp = await message.channel.send("La Amiga computadora esta aqui para ayudarte")

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


    


#    if message.content.startswith("Ultravioleta"):
#        if str(message.author) != "bribot#3950":
#            return
#        print("------------------------")
#        print("Name:Infractions:Clones")
#        
#        tmp = await message.channel.send("------------------------\n Name:Infractions:Clones")
#        for m in clones:
#            print(m + " : " + str(infractions[m])+" : "+str(clones[m]))
#            tmp = await message.channel.send(m + " : " + str(infractions[m])+" : "+str(clones[m]))
#        tmp = await message.channel.send("------------------------")
#        print("------------------------")
#
#        return
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


client.run(credentials.botToken) 
