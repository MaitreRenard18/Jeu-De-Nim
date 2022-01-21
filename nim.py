#! /usr/bin/env python3
from calendar import c
from glob import glob
from PIL import Image
from random import randint
from time import sleep
from tkinter import Image as tkImage
import turtle
import os


def afficher_jeu(nombre_allumettes):
    """Affiche le plateau du jeu.

    :param nombre_allumettes: doit être positif ou nul.
    :type nombre_allumettes: int.
    :param texture: chemin de latexture de l'allumette.
    :type texture: str.
    """
    global wn
    global affichage_jeu

    texture = Image.open(skin_actuel)

    espacement = 10
    largeur_texture, hauteur_texture = texture.size
    largeur_jeu = (largeur_texture + espacement) * nombre_allumettes - espacement
    largeur_jeu = largeur_jeu if largeur_jeu > 0 else 1

    jeu = Image.new("RGBA", (largeur_jeu, hauteur_texture), (255, 255,  255, 0))
    for i in range(nombre_allumettes):
        jeu.paste(texture, (i * (largeur_texture + espacement), 0))
    jeu = jeu.save("Jeu.gif", "GIF", transparency=0)

    wn.addshape("Jeu.gif")
    affichage_jeu.shape("Jeu.gif")


def prise_ia(nombre_allumettes, gagnant_dernier):
    """Implémentation de la statégie gagnante : donne le nombre
    d'allumettes à prendre en fonction de nombre restant et de la
    variante du jeu.

    :param nombre_allumettes: doit être positif ou nul.
    :type nombre_allumettes: int.
    :param gagnant_dernier: indique si celui qui prend la dernière
                            allumette est le gagnant.
    :type gagnant_dernier: bool.
    :returns: nombre d'allumettes à prendre.
    :rtype: int.
    """
    
    if nombre_allumettes <= 4:
        if gagnant_dernier:
            nombre_prendre = 3
        else:
            nombre_prendre = nombre_allumettes - 1
        
        #Vérifie que le resultat est pas en dessous de 0 ou au dessus de 3, sinon sa prend un nombre aléatoire (Car elle panique)
        if nombre_prendre < 1 or nombre_prendre > 3:
            return randint(1, 3)
        elif nombre_prendre > nombre_allumettes:
            return nombre_allumettes
        else:
            return nombre_prendre
    else:
        nombre_prendre = nombre_allumettes % 4

        #Vérifie que le resultat est pas en dessous de 0 ou au dessus de 3, sinon sa prend un nombre aléatoire (Car elle panique)
        if nombre_prendre < 1 or nombre_prendre > 3:
            return randint(1, 3)
        elif nombre_prendre > nombre_allumettes:
            return nombre_allumettes
        else:
            return nombre_prendre


def lancer_partie(ia_joueur_2):
    """Lance une partie du jeu de Nim en solo ou en duo.

    :param ia_joueur_2: indique si le joueur 2 est la machine (True)
                  ou l'utilisateur (False).
    :type ia_joueur_2: bool.
    """
    #Afficher le titre
    global titre
    titre.shape(str(os.getcwd()) + "\\textures\Logo.gif")

    # Enlève le menu
    global menu_boutons
    cacher_boutons(menu_boutons)

    # Pose les questions
    gagnant_dernier = reponse_oui_non("Le gagnant est-il celui qui prend la dernière allumette ?")
    nombre_allumettes = reponse_entier("Avec combien d'allumettes voulez-vous jouer ?", 1, 100)

    # Lancement de la partie
    partie(nombre_allumettes, gagnant_dernier, ia_joueur_2)


def partie(nombre_allumettes, gagnant_dernier, ia_joueur_2):
    """Une seule partie du jeu de Nim.

    :param nombre_allumettes: nombre d'allumettes au début de la partie,
                              doit être positif ou nul.
    :type nombre_allumettes: int.
    :param gagnant_dernier: indique si celui qui prend la dernière
                            allumette est le gagnant.
    :type gagnant_dernier: bool.
    :param ia_joueur_2: indique si le joueur 2 est la machine (True)
                  ou l'utilisateur (False).
    :type ia_joueur_2: bool.
    """
    #Demanque qui joue
    if ia_joueur_2: 
        tour_j1 = reponse_oui_non("Voulez-vous jouer en premier")
    else:
        tour_j1 = True
    
    gagnant = "Personne"

    afficher_jeu(nombre_allumettes)
    
    if not tour_j1:
        if ia_joueur_2:
            sleep(randint(1, 2))
            nombre_allumettes -= prise_ia(nombre_allumettes, gagnant_dernier)
        else:
            nombre_allumettes -= reponse_entier("Joueur 2 : Combien d'allumettes voulez-vous prendre? ", 1, 3)

        if nombre_allumettes <= 0:
                if gagnant_dernier:
                    gagnant = "Joueur 2" if not ia_joueur_2 else "IA"
                else:
                    gagnant = "Joueur 1"
    
    afficher_jeu(nombre_allumettes)  
    
    if nombre_allumettes > 0 :
        while True:
            #Tour du joueur 1
            nombre_allumettes -= reponse_entier("Joueur 1 : Combien d'allumettes voulez-vous prendre? ", 1, 3)
            afficher_jeu(nombre_allumettes)
            
            #Vérifie si J1 a gagner
            if nombre_allumettes <= 0:
                if gagnant_dernier:
                    gagnant = "Joueur 1"
                else:
                    gagnant = "Joueur 2" if not ia_joueur_2 else "IA"
                    
                break
            
            #Tour du joueur 2 / de l'IA
            if ia_joueur_2:
                sleep(randint(1, 2))
                nombre_allumettes -= prise_ia(nombre_allumettes, gagnant_dernier)
            else:
                nombre_allumettes -= reponse_entier("Joueur 2 : Combien d'allumettes voulez-vous prendre? ", 1, 3)
            afficher_jeu(nombre_allumettes)
            
            #Vérifie si J2 a gagner
            if nombre_allumettes <= 0:
                if gagnant_dernier:
                    gagnant = "Joueur 2" if not ia_joueur_2 else "IA"
                else:
                    gagnant = "Joueur 1"
                
                break

    #Affiche le gagnant
    wn.addshape(str(os.getcwd()) + "\\textures\\" + gagnant + ".gif")
    titre.shape(str(os.getcwd()) + "\\textures\\" + gagnant + ".gif")

    #Retourne au menu
    global menu_boutons
    afficher_boutons(menu_boutons)



def creer_menu():
    """Affiche les boutons du menu
    
    :returns: liste contenant tout les boutons du menu.
    :rtype: list.
    """
    
    boutons = []

    solo = creer_bouton(0, 110, str(os.getcwd()) + "\\textures\Solo.gif", lancer_partie, (True))
    boutons.append(solo)
    
    duo = creer_bouton(0, 4, str(os.getcwd()) + "\\textures\Duo.gif", lancer_partie, (False))
    boutons.append(duo)

    global casier_boutons
    casier = creer_bouton(0, -102, str(os.getcwd()) + "\\textures\Casier.gif", afficher_boutons, (casier_boutons))
    boutons.append(casier)

    return boutons

def creer_casier():
    """Créer le casier qui peu en suite etre afficher ou cacher.
    """
    bouttons = []
    x = -150

    global skins
    for skin in skins:
        texture = str(os.getcwd()) + "\skins\\" + skin
        bouttons.append(creer_bouton(x + 50, 0, texture, changer_skin, skin))
        x += 50

    cacher_boutons(bouttons)
    return bouttons

def changer_skin(skin):
    """Change le skin actuel
    """
    global skin_actuel
    skin_actuel = str(os.getcwd()) + "\skins\\" + skin

    global casier_boutons
    global menu_boutons
    cacher_boutons(casier_boutons)
    afficher_boutons(menu_boutons)

def creer_bouton(x, y, texture, fonction, args):
    """ Créer un bouton tout gentil tout mignon.
    
    :param x: position x du bouton.
    :type x: int.
    :param y: position Y du bouton.
    :type y: int.
    :param y: texture du bouton.
    :type y: str.
    :param fonction: fonction à executer lors de l'appui.
    :type fonction: func.
    :param args: paramètres de la fonction à executer lors de l'appui.
    :type fonction: tuple.
    """
    
    wn.addshape(texture)

    bouton = turtle.Turtle()
    bouton.shape(texture)
    bouton.penup()
    bouton.goto(x, y)

    def click(x, y):
        fonction(args)
    bouton.onclick(click, btn=1, add=True)

    return bouton


def afficher_boutons(boutons):
    """affiche les boutons mis en paramètre (liste)
    """
    global menu_boutons
    global casier_boutons
    cacher_boutons(menu_boutons)
    cacher_boutons(casier_boutons)

    for bouton in boutons:
        bouton.showturtle()


def cacher_boutons(boutons):
    """Cache les boutons mis en paramètre (liste)
    """
    for bouton in boutons:
        bouton.hideturtle()


def reponse_oui_non(question):
    """Pose une question binaire (oui/non) à l'utilisateur qui répond
    soit 'o', soit 'n' (éventuellement 'O' ou 'N').
    La question est reposée tant que la réponse n'est pas comprise.

    :param question: la question à poser.
    :type question: str.
    :returns: la réponse sous forme de booléen.
    :rtype: bool.
    """
    
    reponse = turtle.textinput("Question", question)
    if reponse is None:
        return reponse_oui_non(question)
    elif str.lower(reponse) == "o":
        return True
    elif str.lower(reponse) == "n":
        return False
    else:
        return reponse_oui_non(question)


def reponse_entier(question, vmin, vmax):
    """Pose une question à l'utilisateur dont la réponse est un entier
    compris dans l'intervalle [vmin ; vmax]. vmin >= 0.
    La question est reposée tant que la réponse n'est pas correcte.

    :param question: la question à poser.
    :type question: str.
    :param vmin: la valeur minimale possible (>=0).
    :type vmin: int.
    :param vmax: la valeur maximale possible (>= vmin).
    :type vmax: int.
    :returns: l'entier choisi.
    :rtype: int.
    """
    
    nombre = wn.numinput("Question", question, vmin, minval=vmin, maxval=vmax)
    if nombre is None:
        return reponse_entier(question, vmin, vmax)
    else:
        return int(nombre)


def jouer():
    """Lance le jeu de Nim.
    On peut lancer autant d'instances du jeu que l'on souhaite.
    """
    
    global skins
    skins = [file for file in os.listdir(str(os.getcwd()) + "\skins")]

    global skin_actuel
    skin_actuel = str(os.getcwd()) + "\skins\Allumette.gif"
    
    # Créer la fenêtre Turtle
    global wn
    wn = turtle.Screen()
    wn.title("Jeu de Nim")
    wn._root.iconphoto(True, tkImage("photo", file=str(os.getcwd()) + "\\textures\Icon.png"))
    wn.setup(0.5, 0.5)

    #Affiche le titre
    wn.addshape(str(os.getcwd()) + "\\textures\Logo.gif")
    global titre 
    titre = turtle.Turtle()
    titre.shape(str(os.getcwd()) + "\\textures\Logo.gif")
    titre.penup()
    titre.goto(0, 210)

    # Créer l'affichage du jeu (Là ou son afficger les allumettes)
    global affichage_jeu
    affichage_jeu = turtle.Turtle()
    
    # Créer le casier
    global casier_boutons
    casier_boutons = creer_casier()

    # Créer le menu
    global menu_boutons
    menu_boutons = creer_menu()

    turtle.mainloop()


if __name__ == "__main__":
    jouer()