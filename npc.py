#import numpy as np
import random
import discord
import time
import rpgReference as rpg

class generator():
    
    def __init__(self,tDice=4,kDice=3,nStat=6,dice=6,stats=rpg.DNDStats,name="NPC"):
        # TODO: Randomized names
        self.name=name
        self.totalDice=tDice
        self.keepDice=kDice
        self.nStats=nStat
        self.dice=dice
        self.usedRolls=[]
        self.stats=stats
        self.money=0
    
   
    def generate(self,npcTypeName="none"):
        #TODO Separate Classes and Races
        #print("Generating Stats")
        npcType,money=rpg.npcType[npcTypeName]
        stats,self.usedRolls=self.genStats(self.nStats,self.dice)
        #----------------------------------
        #to be removed
        #----------------------------------
        #i=0
        #print("Your rolls were")
        #for used in self.usedRolls:
        #    i+=1
        #    print("Dice %d: " % i+str(used))
        #----------------------------------
        if npcTypeName!="none":
            stats=self.sortStats(stats,npcType)
        i=0
        for s in self.stats:
            self.stats[s]=stats[i]
            #print(s+" : "+str(self.stats[s]))
            i+=1
        self.money=self.genMoney(money)
        return

    def sortStats(self,oStats,npcConf):
        newStats=[]
        for i in npcConf:
            newStats.append(0)
        tmpStats=oStats.copy()
        tmpStats.sort(reverse=1)
        priority=1
        while priority<=len(npcConf):
            #print(priority)
            for current in range(len(npcConf)):
                if npcConf[current][0]==priority:
                    if tmpStats[priority-1]!=0:
                        newStats[current]=tmpStats[priority-1]+npcConf[current][1]
                        tmpStats[priority-1]=0
            priority+=1
        for s in range(len(newStats)):
            while newStats[s]==0:
                r = random.randint(0,len(npcConf)-1)
                #print("-------")
                #print("status %d" % s)
                #print("random=%d"% r)
                #print("Nuevo:%d"%newStats[s])
                #print("Viejo:%d"%tmpStats[r])
                #time.sleep(2)
                newStats[s]=tmpStats[r]
                tmpStats[r]=0
        return newStats

    def genMoney(self,moneyLevel):
        #TODO dice roller
        #multiplier=1
        #addition=0
        moneyLevel=rpg.NORTEMoney[moneyLevel]
        number,faces=moneyLevel.split("d")
        faces,multiplier=faces.split("*")
        stat=0
        for i in range(int(number)):
            stat+=random.randint(1,int(faces))
        stat*=int(multiplier)
        return stat


                
    def genStats(self,n,d):
        stats=[]
        rolls=[]

        for i in range(n):
            stat,roll=self.rollStat(d)
            stats.append(stat)
            rolls.append(roll)
        return stats,rolls
    
    def rollStat(self,d):
        roll=[]
        stat=0
        for i in range(self.totalDice):
            roll.append(random.randint(1,d))
            #print("Die %d: " % i + str(roll[i]))
        roll.sort(reverse=1)
        #print("Keeping:")
        for i in range(self.keepDice):
            stat+=roll[i]
            #print(roll[i])
        #print("Status: %d" % stat)
        return stat,roll

    def randomTable(self,table="races",minDice=1,maxDice=100):
        t = rpg.randomTables[table]
        res = "none"
        v = random.randint(minDice,maxDice)
        res="Dice: %d\n" % v
        for case in t:
            mi,ma=case.split("-")
            if v>=int(mi) and v<=int(ma):
                res+=t[case]
                break
        return res

class npc():

    def __init__(self,name,hp):
        self.name=name
        self.hp=hp

    def damage(self,hit):
        self.hp-=hit
        if self.hp<=0:
            self.die()
        return self.hp

    def heal(self,energy):
        self.hp+=energy
        return self.hp

    def revive(self):
        print(self.name+" It's alive!")
        self.hp=1
        return

    def die(self):
        print(self.name+" it's dead")
        return
