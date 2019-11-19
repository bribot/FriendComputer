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

# TODO: USE BOT API
client = discord.Client()
vat = npc.generator(stats=npc.rpg.NORTEStats)
vatXP = gen.generator()
convos=[]
#log = open("log "+time.ctime,"w+")
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
    print(time.ctime())
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    
    for i in client.guilds:
        print(i)
    print('------')
    await client.change_presence(activity=discord.Game(name="Paranoia"))


@client.event
async def on_message(message):
    
    if message.author.id == client.user.id:
        return
    
    if message.content.startswith("hewwo"):
        print(time.ctime())
        print(message.guild)
        print(message.channel)
        print(message.author)
        print(message.author.dm_channel)
        if message.author.dm_channel == None:
            await message.author.create_dm()
            print(message.author.dm_channel)
        await message.author.dm_channel.send("hewwo")
        print("------------------------")
        

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
    
    if message.content.startswith("!XP"):
        m = ""
        print("---------------------------------------------------")
        print(time.ctime())
        print(message.content)
        mess=message.content[4:]
        print(mess)
#        s=message.content.lower()
#        command,breed  = s.split()
#        r,c,b = breed.split(",")
        m = vatXP.interface(mess)
        print(m)
        if m == "error":
            tmp = await message.channel.send(errorMessage())
        else:
            tmp = await message.channel.send(m)
        
#------------------------------------------------
    if message.content.startswith("!crear"):
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
