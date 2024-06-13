import requetes
from tkinter import *
from tkinter import messagebox

G1 = requetes.json_vers_nx("data_100.txt")

def oracle():
    """
    Interface utilisateur pour explorer les fonctionnalités du module oracle.
    """
    # Actions des boutons pour chaque fonction
    def execute_function():
        selected_function = function_var.get()
        if selected_function == "Trouver collaborateurs communs":
            collab_commun()
        elif selected_function == "Collaborateurs proches":
            collaborateurs_proches()
        elif selected_function == "Vérifier proximité":
            verifier_proximite()
        elif selected_function == "Calculer distance":
            calculer_distance()
        elif selected_function == "Centralité d'un acteur":
            calculer_centralite()
        elif selected_function == "Acteur le plus central":
            trouver_centre_hollywood()
        elif selected_function == "Distance maximale":
            trouver_eloignement_max()
        else:
            messagebox.showerror("Erreur", "Fonction non valide sélectionnée.")

    # Fonctions pour les actions des boutons
    def collab_commun():
        acteur1 = entry_acteur1.get()
        acteur2 = entry_acteur2.get()
        commun = requetes.collab_commun(G1, acteur1, acteur2)
        if commun is None:
            messagebox.showinfo("Collaborateurs communs", f"Impossible de trouver les collaborateurs communs de {acteur1} et {acteur2}.")
        else:
            messagebox.showinfo("Collaborateurs communs", f"Les collaborateurs communs de {acteur1} et {acteur2} sont : {', '.join(commun)}")

    def collaborateurs_proches():
        acteur = entry_acteur1.get()
        k = int(entry_distance.get())
        proches = requetes.collaborateurs_proches(G1, acteur, k)
        if proches is not None:
            messagebox.showinfo("Collaborateurs proches", f"Les acteurs à une distance de {k} ou moins de {acteur} sont : {', '.join(proches)}")
        else:
            messagebox.showinfo("Collaborateurs proches", f"Impossible de trouver les acteurs proches de {acteur}.")

    def verifier_proximite():
        acteur1 = entry_acteur1.get()
        acteur2 = entry_acteur2.get()
        k = int(entry_distance.get())
        if requetes.est_proche(G1, acteur1, acteur2, k):
            messagebox.showinfo("Proximité", f"{acteur1} et {acteur2} sont proches à une distance de {k} ou moins.")
        else:
            messagebox.showinfo("Proximité", f"{acteur1} et {acteur2} ne sont pas proches à une distance de {k} ou moins.")

    def calculer_distance():
        acteur1 = entry_acteur1.get()
        acteur2 = entry_acteur2.get()
        dist = requetes.distance(G1, acteur1, acteur2)
        if dist is not None:
            messagebox.showinfo("Distance", f"La distance entre {acteur1} et {acteur2} est de {dist}.")
        else:
            messagebox.showinfo("Distance", f"Impossible de calculer la distance entre {acteur1} et {acteur2}.")

    def calculer_centralite():
        acteur = entry_acteur1.get()
        centr = requetes.centralite(G1, acteur)
        if centr is not None:
            messagebox.showinfo("Centralité", f"La centralité de l'acteur {acteur} est de {centr}.")
        else:
            messagebox.showinfo("Centralité", f"Impossible de calculer la centralité pour l'acteur {acteur}.")

    def trouver_centre_hollywood():
        centre, centralite = requetes.centre_hollywood(G1)
        messagebox.showinfo("Centre d'Hollywood", f"L'acteur le plus central de Hollywood est {centre} avec une centralité de {centralite}.")

    def trouver_eloignement_max():
        acteur, distance_max = requetes.eloignement_max(G1)
        messagebox.showinfo("Éloignement maximal", f"L'acteur le plus éloigné est {acteur} avec une distance maximale de {distance_max}.")

    # Configuration de l'interface utilisateur avec Tkinter
    root = Tk()
    root.title("Oracle")

    # Menu déroulant pour sélectionner la fonction
    function_options = [
        "Trouver collaborateurs communs",
        "Collaborateurs proches",
        "Vérifier proximité",
        "Calculer distance",
        "Centralité d'un acteur",
        "Acteur le plus central",
        "Distance maximale"
    ]
    function_var = StringVar(root)
    function_var.set(function_options[0])  # Valeur par défaut
    function_menu = OptionMenu(root, function_var, *function_options)
    function_menu.grid(row=0, column=0, columnspan=2, pady=5)

    # Entrées pour les paramètres
    label_acteur1 = Label(root, text="Acteur 1:")
    label_acteur1.grid(row=1, column=0)
    entry_acteur1 = Entry(root)
    entry_acteur1.grid(row=1, column=1)

    label_acteur2 = Label(root, text="Acteur 2:")
    label_acteur2.grid(row=2, column=0)
    entry_acteur2 = Entry(root)
    entry_acteur2.grid(row=2, column=1)

    label_distance = Label(root, text="Distance maximale:")
    label_distance.grid(row=3, column=0)
    entry_distance = Entry(root)
    entry_distance.grid(row=3, column=1)

    # Bouton pour exécuter la fonction sélectionnée
    btn_execute = Button(root, text="Exécuter", command=execute_function)
    btn_execute.grid(row=4, column=0, columnspan=2, pady=5)

    root.mainloop()

# Appel de la fonction oracle pour lancer l'interface utilisateur
oracle()