#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code diffusé aux étudiants de BUT1 dans le cadre de la SAE 2.02: Exploration algorithmique d'un problème.

IUT d'Orleans BUT1 Informatique 2021-2022 
"""
import json
import matplotlib.pyplot as plt
import networkx as nx

# Q1
def renommage(nom):
    """Fonction renvoyant le nom de l'acteur sans les éléments indésirables
    
    Parametres:
        nom: nom de l'acteur
    """
    elem = "[']"
    for x in range(len(elem)):
        nom = nom.replace(elem[x],"")
    v = nom.split("|")
    nom = v[-1]
    return nom

# def json_vers_nx(chemin):
#     """Fonction renvoyant le Graph à partir du chemin d'un fichier texte

#     Parametres:
#         fichier : le chemin d'un fichier.txt
#     """
#     G = nx.Graph()
#     data = open(chemin,'r',encoding = "utf-8")
#     for ligne in data:
#         film = json.loads(ligne)
#         acteurs = film['cast']
#         for i in range(len(acteurs)):
#             for j in range(i + 1, len(acteurs)):
#                 G.add_edge(renommage(acteurs[i]) , renommage(acteurs[j]))
#     nx.draw(G)
#     plt.show()
#     return G   

# json_vers_nx("data_100.txt")
# print(json_vers_nx("data_100.txt").edges)

def convertisseur():
    """Fonction renvoyant le Graph à partir d'un fichier texte

    Parametres:
        fichier : un fichier .txt
    """
    # Création du graph
    G = nx.Graph()
    #Lecture du fichier text
    fic = open('test.txt','r',encoding = "utf-8")
    # Parcour du fichier par ligne
    # for lignes in fic:  
    #     # Initialisation automatique du dictionnaire à partir des données du fichier pour chaque film
    #     dico = json.loads(lignes)
        
    #     # Parcours du dictionnaire des acteurs 
    #     for i in range (len(dico["cast"])):
    #         # Remplace le nom des acteurs et les remets au propre
    #         dico["cast"][i] = enlever_elem(dico["cast"][i])
    #         #S'il n'est pas déjà dans le Graph, le mettre
    #         if dico["cast"][i] not in G:
    #             G.add_node(dico["cast"][i],label='A')

    #     #Pour chaque acteur former un lien entre eux dans le Graph pour signifier qu'ils ont travaillé ensemble 
    #     for acteur1 in dico["cast"]:
    #         for acteur2 in dico["cast"]:
    #             if (acteur1,acteur2) not in G and acteur1 != acteur2:
    #                 G.add_edge(acteur1,acteur2)
    # Dessiner et afficher le Graph

    for ligne in fic:
        film = json.loads(ligne)
        acteurs = film['cast']
        for i in range(len(acteurs)):
            for j in range(i + 1, len(acteurs)):
                G.add_edge(acteurs[i] , acteurs[j])
    nx.draw(G,with_labels = True)
    plt.show()
    return G 

print(convertisseur())


# Q2
def collab_commun(G, acteur1, acteur2):
    """Fonction renvoyant l'ensemble des acteurs ayant collaboré avec acteur1 et acteur2

    Parametres:
        G : le graphe
        acteur1 : un acteur
        acteur2 : un acteur
    """
    return set(G.adj[acteur1]).intersection(G.adj[acteur2])


# Q3
def collaborateurs_proches(G,u,k):
    """Fonction renvoyant l'ensemble des acteurs à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie None si u est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        k: la distance depuis u
    """
    if u not in G.nodes:
        return None
    collaborateurs = set()
    collaborateurs.add(u)
    print(collaborateurs)
    for i in range(k):
        collaborateurs_directs = set()
        for c in collaborateurs:
            for voisin in G.adj[c]:
                if voisin not in collaborateurs:
                    collaborateurs_directs.add(voisin)
        collaborateurs.update(collaborateurs_directs)
    return collaborateurs

def est_proche(G,u,v,k=1):
    """Fonction renvoyant True si l'acteur v est à distance au plus k de l'acteur u dans le graphe G. La fonction renvoie False si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arrivée
        k: la distance depuis u
    """
    if u not in G.nodes or v not in G.nodes:
        return False
    return v in collaborateurs_proches(G,u,k)

# def distance_naive(G,u,v):

def distance(G,u,v):
    """Fonction renvoyant la distance entre l'acteur u et l'acteur v dans le graphe G. La fonction renvoie None si u ou v est absent du graphe.
    
    Parametres:
        G: le graphe
        u: le sommet de départ
        v: le sommet d'arrivée
    """
    if u not in G.nodes or v not in G.nodes:
        return None
    if u == v:
        return 0
    distance = 0
    parcourus = set()
    parcourus.add(u)
    while v not in parcourus:
        distance += 1
        nouveaux = set()
        for c in parcourus:
            for voisin in G.adj[c]:
                if voisin not in parcourus:
                    nouveaux.add(voisin)
        parcourus.update(nouveaux)
        if len(nouveaux) == 0:
            return None
    return distance