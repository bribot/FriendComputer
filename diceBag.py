# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:03:02 2021

@author: Bri
"""
import random as ran

def test():
    # msj = str(ran.randint(1,10))+'+'+str(ran.randint(1,5))+'d'+str(ran.randint(1,20))
    msj= '5*1d4'
    print("Running...")
    print(msj)
    print(reconDice(msj))
    print(rollDice(msj))

def rollDice(msj):
    msj = reconDice(msj)
    msj2=[0,'']
    for m in msj.split('+'):
        if m.isnumeric():
            msj2[0]=msj2[0]+int(m)
            msj2[1]=msj2[1]+m+'+'
        else:
            tmp = eval(m)
            msj2[0] = msj2[0]+tmp[0]
            msj2[1] = msj2[1]+str(tmp[1])+'+'
    msj2[1]=msj2[1][:-1]
    return msj2

def reconDice(msj):
    index=0
    m=msj.split('d')
    while((len(msj.split('d'))-index-1)!=0):
        tmp=-1
        while(True):
            if (tmp+len(m[index])+1)==0 or not m[index][tmp].isnumeric():
                m1 = m[index][tmp+1:]
                break
            tmp-=1
        m[index]=m[index][0:tmp+1]+'getRoll('+m1+','
        tmp=0
        while(True):
            if (tmp-len(m[index+1]))==0 or not m[index+1][tmp].isnumeric():
                m2 = m[index+1][0:tmp]
                break
            tmp+=1
        m[index+1]=m2+')'+m[index+1][tmp:]
        m[index+1]=m[index]+m[index+1]
        msj2=m[index+1]
        m[index]=''
        index+=1
    msj = msj2
    return msj                

def getRoll(ndice, nfaces):
    dice = []
    result = 0
    for n in range(ndice):
        die = ran.randint(1,nfaces)
        dice.append(die)
        result += die
    return result,dice

if __name__ == '__main__':
    main()