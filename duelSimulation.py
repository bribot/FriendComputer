import random
from typing import Literal
attacks = {
    "Fire": ("a","a"),
    "Wind": ("b","a"),
    "Thunder": ("c","a"),
    "Espada": ("a","b"),
    "Hacha": ("b","b"),
    "Lanza": ("c","b"),
    "Arco": ("a","c"),
    "Dagas": ("b","c"),
    "Luz": ("c","c"),
}

attackLiteral = Literal["Espada", "Lanza", "Hacha", "Fire", "Wind", "Thunder", "Dagas", "Arco", "Luz"]

triangle = {
    "Anima": "a",
    "Melee": "b",
    "Specialist": "c"
}

attackAdjectives = {
    "Fire": "uso el flamígero hechizo",
    "Wind": "uso el huracanado hechizo",
    "Thunder": "uso el estruendoso hechizo",
    "Espada": "blandio su",
    "Hacha": "balanceó su",
    "Lanza": "uso su",
    "Arco": "a gran distancia, disparó su",
    "Dagas": "con sigilo, uso sus",
    "Luz": "invocó el poder de las diosas para usar su"
}

foes = {
    # --- Los Héroes (Los Buenos) ---
    "Kael": ('Fire', "Explosión Ígnea", "el joven aprendiz de mago"),
    "Baelin": ('Wind', "Tornado Esmeralda", "el anciano druida que habla con las ardillas"),
    "Thalin": ('Thunder', "Martillo de Runas", "el gerrero enano que forja armas legendarias"),
    "Alaric": ('Espada', "Espada Bendita", "el caballero valiente con una armadura de plata"),
    "Isolde": ('Hacha', "Hacha del Vengador", "la guerrera nórdica que busca vengar a su clan"),
    "Gideon": ('Lanza', "Lanza del Destino", "el paladín de la luz"),
    "Elara": ('Arco', "Flecha de Plata", "la arquera solitaria del bosque"),
    "Sira": ('Dagas', "Dagas de Viento", "la monje ciega que ataca con precisión"),
    "Lyra": ('Luz', "Melodía Sagrada", "la barda viajera cuya música sana heridas"),
    # --- Los Villanos (Los Malos) ---
    "Vexra": ('Fire', "Llama Ponzoñosa", "la hechicera que drena esencia vital"),
    "Nyx": ('Wind', "Vendaval de Envidia", "el espíritu errante"),
    "Malakor": ('Thunder', "Rayo de Vacío", "el señor oscuro"),
    "Mordath": ('Espada', "Hoja de Almas", "el general no-muerto que lidera un ejército eterno"),
    "Skarn": ('Hacha', "Gran Hacha Rota", "el líder orco conocido por su crueldad"),
    "Zaroth": ('Lanza', "Lanza Química", "el alquimista loco que experimenta con mutaciones"),
    "Vorgath": ('Arco', "Flecha Sigilosa", "el asesino a sueldo que nunca falla un tiro en la oscuridad"),
    "Xylos": ('Dagas', "Dagas Sombrías", "el asesino que no deja rastro ni testigos"),
    "Helga": ('Luz', "Destello Corrupto", "la nigromante que profana tumbas buscando artefactos"),
}

triangleAscii='''


              Sword                                 Fire
               / \                                   / \
              /   \                                 /   \
             /     \                               /     \
            ^       v                             ^       v
           /  Melee  \                           / Anima   \
          /           \                         /           \
         /             \                       /             \
      Lance  ---<---  Axe                  Thunder  ---<---  Wind



             Stealth                                  M
               / \                                   / \
              /   \                                 /   \
             /     \                               /     \
            ^       v                             ^       v
           /Specialist\                          /         \
          /            \                        /           \
         /              \                      /             \
      Light   ---<---   Bow                  A    ---<---    S

      
'''


# Diccionario para guardar duelos: {id_retado: {"atacante_id": id, "ataque": "Espada", "channel_id": id}}
activeDuels = {}


def issametriangle(player1, player2):
    if player1[1] == player2[1]:
        return True
    return False

def checkTriangle(player1, player2):
    if issametriangle(player1, player2):
        player1 = player1[0]
        player2 = player2[0]
    else:
        player1 = player1[1]
        player2 = player2[1]
    if player1 == player2:
        return 0
    elif player1 == "a" and player2 == "b":
        return 1
    elif player1 == "b" and player2 == "c":
        return 1
    elif player1 == "c" and player2 == "a":
        return 1
    return 2

def attackExplanation():
    message = "Los ataques tienen dos componentes, el primero es el tipo de ataque, el segundo es el tipo de daño. Si ambos jugadores tienen el mismo tipo de daño, se comparan los tipos de ataque, si no, se comparan los tipos de daño."
    return message #+ "\n" + triangleAscii

def attackMenu():
    message = "Ataques disponibles:\n"
    for attack in attacks:
        message += attack + "\n"
    return message

def attackNarration(player1_name, player2_name, player1, player2, result):
    attack1 = attackAdjectives[player1] + " **" + player1 + "**"
    attack2 = attackAdjectives[player2] + " **" + player2 + "**"
    if result == 0:
        return "%s y %s usaron el mismo ataque, el resultado es un **Empate**." % (player1_name, player2_name)
    elif result == 1:
        return "%s %s y **venció** a %s que %s" % (player1_name, attack1, player2_name, attack2)
    else:
        return "%s %s y **venció** a %s que %s" % (player2_name, attack2, player1_name, attack1)

def playSimulation(player1_name, player2_name, attack1, attack2):
    result = checkTriangle(attacks[attack1], attacks[attack2])
    message = attackNarration(player1_name, player2_name, attack1, attack2, result)
    return result, message

def playSimulation_singleplayer(player_name, attack1):
    player2 = random.choice(list(foes.keys()))
    attack2 = foes[player2][0]
    player2 = f"{player2} {foes[player2][2]}"
    result = checkTriangle(attacks[attack1], attacks[attack2])
    message = attackNarration(player_name, player2, attack1, attack2, result)
    return result, message

def main():
    for i in range(10):
        player1 = random.choice(list(attacks.keys()))
        player2 = random.choice(list(attacks.keys()))
        print(playSimulation_singleplayer("Hiro", player1)[1])
    print(attackExplanation())
    print(attackMenu())
if __name__ == "__main__":
    main()