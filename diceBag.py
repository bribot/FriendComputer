# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:03:02 2021

@author: Bri
"""
import random as ran

def main():
    print("Running...")
    print(reconDice("1d4"))

def rollDice(msj):
    msj = "1d4 + 3"
    msj = "getRoll(1,4) + 3"
    return eval(msj)

def reconDice(msj):
    while(msj.find('d')!=-1):
        temp=msj.split('d')
        
        i = len(temp[0])-1
        if i == 0:
            temp[0] = 'getRoll('+temp[0]+','
        else:
            for j in range(i):
                if not temp[0][i-j].isdigit:
                    temp[0] = temp[0][:i-j+1] + 'getRoll(' + temp[0][i-j+1:] + ','
                    break
        msj = ''.join(temp)
    return temp[0]
                    

def getRoll(ndice, nfaces):
    dice = []
    result = 0
    for n in range(ndice):
        die = ran.randint(1,nfaces)
        dice.append(die)
        result += die
    return result

if __name__ == '__main__':
    main()