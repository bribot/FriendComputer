# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:03:02 2021

@author: Bri
"""
import random as ran

specialCommands = ['u','l']

def test():
    msj = '2d20l'
    # msj= ''
    # nrolls = ran.randint(1,10)
    # for i in range(nrolls):
    #     msj += str(ran.randint(1,5))+'d'+str(ran.randint(1,20)) + '+'
    # msj += str(ran.randint(-10,10))
    print("Running...")
    print(msj)
    print(rollDice(msj))

def rollDice(msj):
    msj = reconDice(msj)
    msj2 = eval(msj)
    return [msj2,msj]


def reconDice(msj):
    mes = msj.split('d')
    nRoll = len(mes)-1
    result = ''
    facedice = 0
    dice = -1
    face = -1
    for m in mes:
        m1=''
        m2=''
        if(facedice == 1):
            while(facedice == 1):
                if(len(m)>0 and m[0].isnumeric()):
                    temp,m = m[0],m[1:]
                    m2 = m2+temp
                else:
                    face = int(m2)
                    if(len(m)>0 and m[0] in specialCommands):
                        temp,m = m[0],m[1:]
                        sp = temp
                    else:
                        temp = ''
                    mR = getRoll(dice,face,temp)
                    dice = -1
                    face = -1
                    result = result + mR
                    nRoll-=1
                    facedice = 0
                
            facedice = 0 if nRoll>0 else 1
        if(facedice == 0):
            while(facedice == 0):
                if(len(m)>0 and m[-1].isnumeric()):
                    temp,m = m[-1],m[:-1]
                    m1 = temp+m1
                else:
                    dice = int(m1)
                    facedice = 1
        result = result + m
        
    return result

                    

def getRoll(ndice, nfaces, special = ''):
    dice = []
    result = '('
    for n in range(ndice):
        die = ran.randint(1,nfaces)
        dice.append(die)
        result += str(die) + "+"
    result = result[0:-1]
    result += ")"
    if(special == specialCommands[0]):
        result = 'max'+result
        result = result.replace('+',',')
    elif(special == specialCommands[1]):
        result = 'min'+result
        result = result.replace('+',',')
    return result#,dice

if __name__ == '__main__':
    test()