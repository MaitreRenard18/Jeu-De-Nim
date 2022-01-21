#! /usr/bin/env python3
from PIL import Image
from random import randint
from time import sleep
from tkinter import Image as tkImage
import turtle
import os


def afficher_jeu(nombre_allumettes, texture=str(os.getcwd()) + "\skins\Allumette.gif"):
    """Affiche le plateau du jeu.

    :param nombre_allumettes: doit être positif ou nul.
    :type nombre_allumettes: int.
    :param texture: chemin de latexture de l'allumette.
    :type texture: str.
    """
    texture = Image.open(texture)

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
        else:
            return nombre_prendre
    else:
        nombre_prendre = nombre_allumettes % 4

        #Vérifie que le resultat est pas en dessous de 0 ou au dessus de 3, sinon sa prend un nombre aléatoire (Car elle panique)
        if nombre_prendre < 1 or nombre_prendre > 3:
            return randint(1, 3)
        else:
            return nombre_prendre


def lancer_partie(ia_joueur_2):
    """Lance une partie du jeu de Nim en solo ou en duo.

    :param ia_joueur_2: indique si le joueur 2 est la machine (True)
                  ou l'utilisateur (False).
    :type ia_joueur_2: bool.
    """

    # Enlève le menu
    cacher_menu()

    # Pose les questions
    gagnant_dernier = reponse_oui_non("Le gagnant est-il celui qui prend la dernière allumette ? ")
    nombre_allumettes = reponse_entier("Avec combien d'allumettes voulez-vous jouer ? ", 1, 100)

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

    tour_j1 = reponse_oui_non("Voulez-vous jouer en premier ? ") #Je renseigne dans une variable le joueur qui commencera à jouer.
    gagnant = "Personne" #Je créer une variable pour renseigner le nom du gagnant.

    afficher_jeu(nombre_allumettes)
    
    if not tour_j1: #Si on ne joue pas en premier, et que l'on joue contre une IA, le nombre d'allumettes est diminué de l'entier sortie de prise_ia
        if ia_joueur_2:
            sleep(randint(1, 2))
            nombre_allumettes -= prise_ia(nombre_allumettes, gagnant_dernier)
        else: #Si on joue contre une humain, on pose la question au joueur 2, et le nombre d'allumettes est diminué de l'entier choisi
            nombre_allumettes -= reponse_entier("Joueur 2 : Combien d'allumettes voulez-vous prendre ? ", 1, 3)
        afficher_jeu(nombre_allumettes)

    while True:
        #Tour du joueur 1
        nombre_allumettes -= reponse_entier("Joueur 1 : Combien d'allumettes voulez-vous prendre ? ", 1, 3) #On pose la question au joueur 1, et le nb d'allumette est diminué
        afficher_jeu(nombre_allumettes)
        
        #Vérifie si J1 a gagner
        if nombre_allumettes <= 0:
            if gagnant_dernier: #Si gagnant dernier est True, attribu le joueur 1 à gagnant, sinon, on attribu le joueur 2/IA à gagnant
                gagnant = "Joueur 1"
            else:
                gagnant = "Joueur 2" if not ia_joueur_2 else "IA"
                
            break
        
        #Tour du joueur 2 / de l'IA
        if ia_joueur_2: 
            sleep(randint(1, 2))
            nombre_allumettes -= prise_ia(nombre_allumettes, gagnant_dernier) #on diminue le nombre d'allumettes par l'entier qui sort de prise ia
        else:
            nombre_allumettes -= reponse_entier("Joueur 2 : Combien d'allumettes voulez-vous prendre ? ", 1, 3) #Ou alors on pose la question au joueur 2
        afficher_jeu(nombre_allumettes)
        
        #Vérifie si J2 a gagner
        if nombre_allumettes <= 0: #Ici, inverssement à avant, on attribu gagnant à joueur 2/IA, ou alors à joueur 1, selon gagnant dernier
            if gagnant_dernier:
                gagnant = "Joueur 2" if not ia_joueur_2 else "IA"
            else:
                gagnant = "Joueur 1"
            
            break

    #Affiche le gagnant
    print(gagnant + " a gagner !") #On annonce le gagnant


def creer_menu():
    """Affiche les boutons du menu
    
    :returns: liste contenant tout les boutons du menu.
    :rtype: list.
    """
    
    boutons = []

    solo = creer_bouton(0, 110, str(os.getcwd()) + r"\textures\Solo.gif", lancer_partie, (True))
    boutons.append(solo)
    
    duo = creer_bouton(0, 4, str(os.getcwd()) + r"\textures\Duo.gif", lancer_partie, (False))
    boutons.append(duo)

    casier = creer_bouton(0, -102, str(os.getcwd()) + r"\textures\Casier.gif", None, None)
    boutons.append(casier)
    
    boutique = creer_bouton(0, -208, str(os.getcwd()) + r"\textures\Boutique.gif", None, None)
    boutons.append(boutique)

    return boutons


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


def afficher_menu():
    for bouton in boutons:
        bouton.showturtle()


def cacher_menu():
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
    L'utilisateur a le choix de rejouer à chaque fin de partie.
    """

    # affichage de la partie
    global wn
    wn = turtle.Screen()
    wn.title("Jeu de Nim")
    wn._root.iconphoto(True, tkImage("photo", file=str(os.getcwd()) + r"\textures\Icon.png"))
    wn.setup(0.5, 0.5)

    global affichage_jeu
    affichage_jeu = turtle.Turtle()
    
    while True:
        # paramètres de la partie
        ia_joueur_2 = reponse_oui_non("Voulez-vous jouer contre la machine ? ")
        gagnant_dernier = reponse_oui_non(
            "Le gagnant est-il celui qui prend la dernière allumette ? ")
        nombre_allumettes = reponse_entier("Avec combien d'allumettes voulez-vous jouer ? ", 1, 100)

        # lancement de la partie
        partie(nombre_allumettes, gagnant_dernier, ia_joueur_2)

        # on rejoue ?
        afficher_jeu(nombre_allumettes)
        if not reponse_oui_non("Voulez-vous rejouer ? "):
            break


def print_skins():
    skins_dir = str(os.getcwd()) + "\skins"
    
    for file in os.listdir(skins_dir):
        if file.endswith(".gif"):
            skin = Image.open(os.path.join(skins_dir, file))
            afficher_jeu(16, skin)


if __name__ == "__main__":
    # si le programme est exécuté directement, on lance une partie

    # Créer la fenêtre Turtle
    global wn
    wn = turtle.Screen()
    wn.title("Jeu de Nim")
    wn._root.iconphoto(True, tkImage("photo", file=str(os.getcwd()) + r"\textures\Icon.png"))
    wn.setup(0.5, 0.5)

    # Créer l'affichage du jeu (Là ou son afficger les allumettes)
    global affichage_jeu
    affichage_jeu = turtle.Turtle()
    
    # Créer le menu
    global boutons
    boutons = creer_menu()

    turtle.mainloop()
