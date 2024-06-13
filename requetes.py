#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""
import json
import networkx as nx

# Q1
def renommage(nom):
    """Fonction renvoyant le nom de l'acteur sans les éléments indésirables
    
    Parametres:
        nom: nom de l'acteur
    """
    elem = "[']"
    for x in elem:
        nom = nom.replace(x,"")
    v = nom.split("|")
    nom = v[-1]
    return nom

def json_vers_nx(chemin):
    """Fonction renvoyant le Graph à partir du chemin d'un fichier texte

    Parametres:
        fichier : le chemin d'un fichier.txt
    """
    G = nx.Graph()
    data = open(chemin,'r',encoding = "utf-8")
    for ligne in data:
        film = json.loads(ligne)
        acteurs = film['cast']
        for i in range(len(acteurs)):
            for j in range(i + 1, len(acteurs)):
                G.add_edge(renommage(acteurs[i]) , renommage(acteurs[j]))
    # nx.draw(G)
    # plt.show()
    return G   

G1 = json_vers_nx("data_100.txt")

# print(json_vers_nx("data_100.txt"))
# print(json_vers_nx("data_100.txt").nodes)


# Q2
def collab_commun(G, acteur1, acteur2):
    """Fonction renvoyant l'ensemble des acteurs ayant collaboré avec acteur1 et acteur2

    Parametres:
        G : le graphe
        acteur1 : un acteur
        acteur2 : un acteur
    """
    if acteur1 not in G.nodes or acteur2 not in G.nodes:
        return None
    return set(G.neighbors(acteur1)).intersection(G.neighbors(acteur2))

# print(collab_commun(G1, "Toto", "Titi"))


# Q3
def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    collaborateurs = {u}
    proches = set(G.neighbors(u))  # Initialisation avec les voisins directs
    while k > 0:
        collaborateurs.update(proches)
        nouveaux_proches = set()
        for c in proches:
            nouveaux_proches.update(set(G.neighbors(c)) - collaborateurs)
        proches = nouveaux_proches
        k -= 1
    return collaborateurs

# print(collaborateurs_proches(G1,"Toto",0)) # {'Toto'}
# print(collaborateurs_proches(G1,"Toto",1)) # {'Tata', 'Toto'}
# print(collaborateurs_proches(G1,"Toto",2)) # {'Toto', 'Titi', 'Tata'}
# print(collaborateurs_proches(G1,"Toto",3)) # {'Titi', 'Toto', 'Tata', 'Tutu'}


def est_proche(G,u,v,k=1):
    """Fonction renvoyant True si l'acteur v est à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie False si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arrivée
        k: la distance depuis u
    """
    return v in collaborateurs_proches(G,u,k)

# print(est_proche(G1,"Toto","Tata",0)) # False
# print(est_proche(G1,"Toto","Tata",1)) # True


def distance(G,u,v):
    """Fonction renvoyant la distance entre l'acteur u et l'acteur v dans le graphe G. La fonction renvoie None si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arrivée
    """
    if u == v:
        return 0
    distance = 0
    parcourus = {u}
    while v not in parcourus:
        distance += 1
        nouveaux = set()
        for c in parcourus:
            for voisin in G.neighbors(c):
                if voisin not in parcourus:
                    nouveaux.add(voisin)
        parcourus.update(nouveaux)
        if len(nouveaux) == 0:
            return None
    return distance

# print(distance(G1,"Toto","Tata")) # 1
# print(distance(G1,"Toto","Titi")) # 2
# print(distance(G1,"Toto","Tutu")) # 3
# print(distance(G1,"Tata","Titi")) # 1


def centralite(G, u):
    """
    Calcule la centralité d'un acteur, c'est-à-dire la plus grande distance entre cet acteur et tous les autres acteurs du graphe.
    
    :param G: Graphe Networkx des collaborations.
    :param u: Acteur/actrice pour lequel on calcule la centralité.
    :return: Centralité de l'acteur ou None si l'acteur n'est pas dans le graphe.
    """
    visites = {u}
    noeud_actuels = {u}
    max_distance = 0
    while noeud_actuels:
        prochain_noeud = set()
        nouveau_voisin_trouve = False
        for acteur in noeud_actuels:
            for voisin in G.neighbors(acteur):
                if voisin not in visites:
                    prochain_noeud.add(voisin)
                    visites.add(voisin)
                    nouveau_voisin_trouve = True
        if nouveau_voisin_trouve:
            max_distance += 1
        noeud_actuels = prochain_noeud
    return max_distance

# print(centralite(G1, "Toto")) # 3


def centre_hollywood(G):
    """
    Détermine l'acteur le plus central du graphe, c'est-à-dire celui avec la plus petite centralité.
    
    :param G: Graphe Networkx des collaborations.
    :return: Acteur le plus central du graphe.
    """
    centralites = {u: centralite(G, u) for u in G.nodes()}
    acteur_central = min(centralites, key=centralites.get)
    centralite_max = centralites[acteur_central]
    return acteur_central, centralite_max

# print(centre_hollywood(G1)) # ('Tata', 2)


def eloignement_max(G):
    """
    Calcule la distance maximale entre deux acteurs dans le graphe.
    
    :param G: Graphe Networkx des collaborations.
    :return: Distance maximale entre deux acteurs.
    """
    centralites = {u: centralite(G, u) for u in G.nodes()}
    acteur_peripherique = max(centralites, key=centralites.get)
    centralite_min = centralites[acteur_peripherique]
    return acteur_peripherique, centralite_min

# print(eloignement_max(G1)) # ('Toto', 3)