# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:19:05 2021

@author: Bri
"""

import random as ran
import csv
import os


path = "./Tables"
file = "gatchaTama.csv"

def rollGatcha():
    if not checkTable(path+file):
        return "Error: Tabla no encontrada, esto es tu culpa"  
    table = loadTable()
    dice = ran.randint(0,len(table)-1)
    #result = 'Sacaste un ' +str(dice+1)
    result = table[dice]
    return result

def loadTable():
    with open(path+file,encoding="ISO-8859-1") as infile:
        reader = csv.reader(infile)
        table = [rows[0] for rows in reader]
    return table


def checkTable(name):
    if name+'.csv' in os.listdir(path):
        return 1
    else:
        return 0