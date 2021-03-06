# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 01:55:21 2020

@author: Bri
"""

import os
import csv
import random as ran

path="./Tables/"

index = {}

# def main():
#     print("code me daddy OwO")
            
            
def rollTable(name):
    if not checkTable(name):
        return "Error: Tabla no encontrada, esto es tu culpa"  
    table = loadTable(name)
    dice = ran.randint(0,len(table)-1)
    result = 'Sacaste un ' +str(dice+1)
    result += '\n'+table[dice]
    return result

def loadTable(file):
    with open(path+file+'.csv',encoding="ISO-8859-1") as infile:
        reader = csv.reader(infile)
        table = [rows[0] for rows in reader]
    return table

def tableIndex():
    result='Tablas disponibles'
    for file in os.listdir(path):
        result+='\n'+file.split('.')[0]
    return result

def checkTable(name):
    if name+'.csv' in os.listdir(path):
        return 1
    else:
        return 0
            
# if __name__ == "__main__":
#     main()
    
# juergas =( "Has perdido un diente, tira 1d10: 1-3 una muela, 4-6 un premolar, 7-8 un incisivo, 9-10 una paleta",
# "Has perdido un dedo, tira 1d10: 1-3 meñique, 4-6 anular, 7-8 corazón, 9 indice, 10 pulgar",
# "Nuevo tatuaje, tira 1d10: 1-2 del asco, 3-6 meh, 6-8 bueno, 9-10 super guay",
# "Felicidades, seras papá/mamá",
# "Enhorabuena por tu boda","Alguien en un grupo criminal te debe un favor",
# "Hay una recompensa por tu cabeza",
# "Ganaste una apuesta, tira 1d10 para ver tus ganancias: 1-4 1d100 oros, 5-7 2d100 oros, 8-9 4d100 oros, 10 1 punto de fortuna",
# "Obtienes 1d10 fama",
# "Pierdes 1d4 honor",
# "Apareces en otro pueblo",
# "Amaneces en una fuente o pozo",
# "Despiertas en la carsel, con la tarjeta de Agusti Gomelez en el bolsillo",
# "Despiertas desnudo con 1d10 hombre, 1d10 mujeres",
# "Un goblin te sigue a todos lado llamándote Jefe",
# "Amaneces desnudo junto a un animal",
# "Pierdes una apuesta, pierdes 1d10x100 oros",
# "Despiertas cubierto de sangre, no te preocupes, no es tuya",
# "Despiertas desnudo con un hombre",
# "Despiertas desnudo con una mujer",
# "¿Qué hace ese bebé en tus brazos?",
# "Amaneces envuelto en una piel de un animal, aún esta fresca y tu cuerpo esta lleno de heridas, pierdes 1d4 de puntos de vida",
# "Felicidades, te uniste al circo",
# "Tienes una dirección anotada en la mano, tira 1d6: 1-2 un duelo, 3-4 el lugar de una cita, 5-6, una emboscada",
# "¿Cuando llegaste a las alcantarillas?",
# "Despiertas con una bagatela",
# "Despiertas con una carga ilegal",
# "De tanto alcohol has desarrollado una resistencia increíble a venenos, tienes resistencia a venenos por una semana",
# "Conociste a tu pareja soñada, o fue solo un sueño",
# "Durante tu borrachera hiciste algo que agrado a los dioses, elige un truco divino y puedes usarlo una vez durante la siguiente semana, si eres clérigo obtienes un espacio extra de conjuro de nivel 1",
# "Despiertas en un templo, todo esta roto, y un sacerdote te mira de mala manera",
# "Despiertas con la peor resaca, 1 nivel de fatiga",
# "Despiertas con una cabeza en tus manos",
# "Tienes un corte en la mano, a tu lado alguien te mira orgulloso con un corte en su mano",
# "Ofendiste a un brujo o hechicero y te maldijo, tira 1d6: 1-2 solo fueron palabras, 3-4 la maldición es autentica, 5-6, la maldición es algo terrible",
# "Hiciste buenas migas con un brujo o hechicero, tira 1d6: 1-2 solo fueron palabra, 3-4 recibe ventaja en una tirada a tu elección, 5-6 cuando caigas en 0 pv, recuperas 1d10 puntos de golpe",
# "Un montón de niños (2d6) te sigue a todos lados llamándote papá",
# "Probaste un licor azul que hizo que recordaras el momento más feliz de tu vida",
# "Durante una semana, cada efecto de curación mágica te cura lo máximo, aunque tu cabello crece 2d4 pulgadas cada que te curas",
# "Durante la euforia alcohólica te uniste a un culto religioso, tienes símbolos sagrados de la deidad",
# "La ciudad esta llena de carteles de Se busca, vivo o muerto con una recompensa de 1d100+100 oros por ti",
# "Durante los festejos le salvaste la vida a un tipo y ahora te debe un favor, tira 1d6: 1 un ladrón, 2, un sacerdote, 3 un aprendiz de mago, 4 un soldado, 5 un enano, 6 un explorador","Despiertas en un cepo, tienes lleno el cuerpo de inmundicias",
# "En la juerga te encuentras con un forastero de tierras lejanas y se pasa la noche hablandote de tierras lejanas, al final te entrega un papel arrugado escrito en un idioma desconocido para ti","Un animal te detesta, y te perseguirá para hacerte la vida imposible, nunca podrás alcanzarlo por más que te esfuerces, y se encargara de hacerte la vida imposible","Durante la fiesta te hiciste algo en la boca, durante una semana cada que tu personaje hable debes hacerlo con la lengua fuera","Te encuentras en la sala de una villa noble","A pesar de la fiesta, amaneces completamente recuperado, tranquilo y con una gran paz interior","Eres el nuevo miembro de una secta","Un animalito se ha encariñado contigo, te seguirá a todos lados y te defenderá con su vida","Te despiertas en el lugar más alto del poblado","Un animalito te sigue a todos lados, es gracioso y adorable, pero extremadamente ruidoso, te seguirá a todos lados","Obtienes una medalla de héroe de guerra","Anoche bebiste tanto, que ahora una gran parte de tu sangre es alcohol, todo el daño causado por armas cortantes, contundentes y ṕerforantes te hacen la mitad de daño, pero el fuego te hace el doble de daño","Tienes los dedos llenos de anillos y una corona en la cabeza, parece ser oro, pero si lo rallas con la uña es solo pintura","Un joven te sigue, admirado por tu grandeza, sirviéndote como porta antorchas","Tuviste una pelea abrumadora, amaneces con la mitad de tus puntos de golpe","Amaneces atado de pies y manos","La noche pasada te cruzaste con un adivino, que te leyó la fortuna, pídele al Narrador que te de un presagio","Despiertas dentro de una casa, afuera una multitud con antorchas grita: ¡Sal criatura de los infiernos!","Anoche saliste muy animado, pero en tu furor has olvidado algo, tira 1d6: 1 tu arma, 2 tu escudo, 3 tu armadura, 4-5 tu tesoro, 6 tu barba o cabello","Hiciste enojar a un mago poderoso y de muy poca paciencia, ahora una parte de tu cuerpo se ve igual a la de un animal. Tira 1d10: 1-2 tu cabeza, 3 tu brazo izquierdo, 4 tu brazo derecho, 5 tu pierna izquierda, 6 tu pierna derecha, 7-8 tu nueva y flamante cola, 9 solo tu rostro, 10 eres un animalito, pero puedes hablar","Despiertas con una marca de un poderoso demonio en tu cuerpo, tira 1d10: 1-2 muy visible, 3-4 visible, pero puedes taparla, 5-6 poco visible, 7-8 casi oculto, 9-10 ¿quién te va a mirar ahí?","Despiertas con un pergamino en la mano. Se trata de un plan para matar a alguien muy importante","Has ofendido a un muy poderoso mercader, durante un mes, todo te costara el doble o triple","Una joven doncella esta a tu lado, jura que la salvaste de un poderoso ser, y ahora debes protegerla","Despiertas con un objeto extraño, parece valioso y poderoso","Un tipo de aspecto muy extraño te entrego una hermosa bola de pelo con ojos, te dijo algo que no bañarlo pasando la media noche y no alimentarlo,  o era al revés","Un grupo de personas ha determinado que eres la reencarnación de un héroe legendario, te seguirán hasta la muerte, o hasta que demuestres ser un fraude","Despiertas junto a un cadáver (¿o no?)"
# )