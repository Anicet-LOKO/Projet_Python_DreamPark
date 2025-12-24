"""
Interface Graphique Utilisateur (GUI) du DreamPark.

Ce module centralise l'affichage du tableau de bord (recettes, places libres)
et gère les interactions utilisateur pour les entrées, sorties et l'administration.

Auteur : Anicet-Darcia
"""

import tkinter as tk
from tkinter import messagebox, simpledialog

class DreamParkGUI:
    """
    Classe principale de l'interface graphique.

    Orchestre la communication entre l'utilisateur et les modules métiers,
    infrastructure et gestion de données.
    """

    def __init__(self, root, park, db):
        """
        Initialise la fenêtre principale et construit les composants graphiques.

        Args:
            root (tk.Tk): La fenêtre racine de l'application.
            park (ParcDeStationnement): L'instance du moteur de parking.
            db (GestionnaireClients): L'instance de la base de données.
        """
        self.root = root
        self.park = park
        self.db = db
        self.actifs = {} 

        self.root.title("PROJET DreamPark - Gestionnaire de Stationnement")
        self.root.geometry("650x700")
        self.root.configure(bg="#2c3e50")

        # --- Dashboard (CA et Places) ---
        self.frame_top = tk.Frame(root, bg="#34495e", pady=15)
        self.frame_top.pack(fill="x")
        
        self.lbl_ca = tk.Label(self.frame_top, text="", font=("Courier", 16, "bold"), fg="#2ecc71", bg="#34495e")
        self.lbl_ca.pack()

        self.lbl_dispo = tk.Label(self.frame_top, text="", font=("Arial", 12, "bold"), fg="white", bg="#34495e")
        self.lbl_dispo.pack()

        # --- Panneau d'informations (Contraintes) ---
        self.frame_info = tk.LabelFrame(root, text=" Rappel des contraintes ", fg="white", bg="#2c3e50", padx=10, pady=10)
        self.frame_info.pack(pady=10, padx=50, fill="x")
        
        info_text = "Format Plaque : AA1234\nHauteur Max : 2.50m | Longueur Max : 5.00m"
        tk.Label(self.frame_info, text=info_text, fg="#bdc3c7", bg="#2c3e50", justify="left").pack()

        # --- Boutons d'action ---
        btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "height": 2}
        
        tk.Button(root, text="ENTRÉE PORTAIL NORD", bg="#2980b9", **btn_style,
                  command=lambda: self.entree("N")).pack(pady=5, padx=100, fill="x")
        
        tk.Button(root, text="ENTRÉE PORTAIL SUD", bg="#3498db", **btn_style,
                  command=lambda: self.entree("S")).pack(pady=5, padx=100, fill="x")

        tk.Button(root, text="SORTIE & PAIEMENT", bg="#e67e22", **btn_style,
                  command=self.sortie).pack(pady=10, padx=100, fill="x")

        # --- Bouton de Gestion Administrative ---
        tk.Button(root, text="GESTION DES CONTRATS (Admin)", bg="#9b59b6", **btn_style,
                  command=self.ouvrir_gestion_contrats).pack(pady=5, padx=100, fill="x")

        # --- Registre Visuel ---
        tk.Label(root, text="VÉHICULES ACTUELLEMENT GARÉS", bg="#2c3e50", fg="white", font=("Arial", 9, "italic")).pack(pady=(10,0))
        self.listbox = tk.Listbox(root, height=6, width=65, font=("Courier New", 10))
        self.listbox.pack(pady=5)

        # --- Bouton Quitter ---
        tk.Button(root, text="QUITTER L'APPLICATION", bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                  command=self.quitter).pack(pady=20)

        self.maj_interface()

    def maj_interface(self):
        """
        Rafraîchit les éléments visuels du tableau de bord.
        Met à jour le compteur de places, les recettes et la liste des véhicules garés.
        """
        self.lbl_ca.config(text=f"RECETTES : {self.park.chiffre_affaire_total:.2f} €")
        self.lbl_dispo.config(text=f"PLACES LIBRES : {self.park.compteur_global} / 5")
        
        self.listbox.delete(0, tk.END)
        for plaque, id_p in self.actifs.items():
            u = self.db.rechercher_par_plaque(plaque)
            
            if u.services_actifs:
                txt_services = f" | SERVICES: {', '.join(u.services_actifs)}"
            else:
                txt_services = " | Sans service"
            
            if u.type_offre == "Pack Garanti":
                type_c = "[VIP]"
            else:
                type_c = f"[{u.type_offre[:3].upper()}]" # Affiche [STA] ou [ABO]
            # affichage du nomdu client avec son type d'offre
            self.listbox.insert(tk.END, f" {type_c} {plaque} ({u.nom}) -> {id_p}{txt_services}")

    def ouvrir_gestion_contrats(self):
        """
        Déclenche l'ouverture d'une fenêtre secondaire (Toplevel).
        Permet de modifier les abonnements des clients enregistrés.
        """
        top = tk.Toplevel(self.root)
        top.title("Admin : Gestion des Offres")
        top.geometry("450x450")
        top.configure(bg="#ecf0f1")

        tk.Label(top, text="Liste des clients enregistrés :", bg="#ecf0f1", font=("Arial", 10, "bold")).pack(pady=10)
        
        lb_clients = tk.Listbox(top, height=10, width=55)
        lb_clients.pack(pady=5, padx=10)
        
        for p, c in self.db.annuaire.items():
            lb_clients.insert(tk.END, f"{p} - {c.nom} ({c.type_offre})")

        def changer_statut(nouveau_statut):
            selection = lb_clients.curselection()
            if not selection:
                messagebox.showwarning("Admin", "Veuillez sélectionner un client.")
                return
            
            plaque = lb_clients.get(selection[0]).split(" - ")[0]
            usager = self.db.rechercher_par_plaque(plaque)
            usager.souscrire_offre(nouveau_statut)
            self.db.sauvegarder_donnees()
            
            messagebox.showinfo("Succès", f"{usager.nom} est passé en : {nouveau_statut}")
            top.destroy()
            self.maj_interface()

        tk.Button(top, text="Passer en STANDARD", command=lambda: changer_statut("Standard"), bg="#95a5a6", width=30).pack(pady=2)
        tk.Button(top, text="Passer en ABONNÉ", command=lambda: changer_statut("Abonné"), bg="#3498db", fg="white", width=30).pack(pady=2)
        tk.Button(top, text="Abonné passer en PACK GARANTI", command=lambda: changer_statut("Pack Garanti"), bg="#f1c40f", width=30).pack(pady=2)

    def entree(self, zone):
        """
        Gère le processus d'entrée d'un véhicule.
        
        Args:
            zone (str): "N" pour Nord, "S" pour Sud.
        """
        try:
            plaque = simpledialog.askstring("Caméra", "Scannez la plaque (Modèle: AA1234) :")
            if not plaque: return 
            plaque = plaque.upper().strip()

            if plaque in self.actifs:
                messagebox.showwarning("Erreur", "Véhicule déjà détecté.")
                return

            from infrastructure import BorneDAcces
            borne = BorneDAcces(f"B_{zone}", "Nord" if zone=="N" else "Sud", self.park, self.db)
            res = borne.traiter_vehicule(plaque)

            if res == "ERREUR_PLAQUE":
                messagebox.showerror("Format", "Plaque incorrecte !")
            elif res == "PARTENAIRE":
                messagebox.showinfo("Pack Garanti", "Parking plein. Redirection offerte.")
            elif res == "PLEIN":
                messagebox.showwarning("Refus", "Parking complet.")
            elif res:
                self.actifs[plaque] = res
                messagebox.showinfo("Bienvenue", f"Accès autorisé !\nPlace : {res}")
                self.maj_interface()
                
        except Exception as e:
            messagebox.showerror("Erreur Système", str(e))

    def sortie(self):
        """
        Gère le processus de sortie, le paiement et la libération de la place.
        """
        try:
            plaque = simpledialog.askstring("Sortie", "Plaque du véhicule :")
            if not plaque: return
            plaque = plaque.upper().strip()

            if plaque in self.actifs:
                id_p = self.actifs[plaque]
                from infrastructure import BorneDAcces
                borne = BorneDAcces("B_SORTIE", "Sortie", self.park, self.db)
                borne.gerer_fin_stationnement(plaque)

                if self.park.liberer_une_place(id_p):
                    del self.actifs[plaque]
                    self.maj_interface()
                    messagebox.showinfo("Facture", "Paiement validé. Barrière ouverte.")
            else:
                messagebox.showerror("Erreur", "Véhicule non trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def quitter(self):
        """Ferme proprement l'application après confirmation."""
        if messagebox.askyesno("Quitter", "Voulez-vous quitter ?"):
            self.root.destroy()