"""
Module infrastructure et capteurs du DreamPark.

Ce module simule les composants matériels physiques (capteurs laser, caméras, 
automates de transport); ici on va définir la logique de la Borne d'Accès.

Auteur : Anicet-Darcia
"""

import re
import tkinter.simpledialog as sd
from tkinter import messagebox
from gestion_clients import Client
from services import Livraison, Maintenance

# --- CLASSES MATÉRIELLES ---

class Camera:
    """Simule une caméra de lecture automatique de plaques d'immatriculation (LAPI)."""
    
    def scanner_plaque(self, plaque):
        """Simule le scan optique d'une plaque."""
        return f"SCAN_SUCCESS: {plaque}"

    def mesurer_gabarit(self):
        """Simule la mesure automatique du véhicule par les capteurs."""
        return 2.10, 4.50 

class Teleporteur:
    """Simule l'automate de transport robotisé qui déplace les véhicules vers les places."""
    
    def deplacer_vers(self, id_place):
        """Simule le mouvement de l'automate."""
        return f"Mouvement automate vers {id_place} terminé."

class BorneTicket:
    """Gère l'impression physique des tickets de stationnement."""
    
    def imprimer_ticket(self, plaque, place):
        """Génère le texte d'un ticket papier."""
        return f"TICKET DREAM PARK\nVéhicule: {plaque}\nPlace: {place}\nDate: 2024"

# --- MISE À JOUR DE LA BORNE D'ACCES ---

class BorneDAcces:
    """
    Interface principale entre le matériel et le système métier.
    
    Cette classe orchestre l'entrée et la sortie des véhicules en utilisant 
    les périphériques (caméra, automate, distributeur).
    """

    def __init__(self, nom_borne, secteur, parking_objet, base_clients):
        """
        Initialise la borne avec ses périphériques matériels.

        Args:
            nom_borne (str): Identifiant de la borne.
            secteur (str): Localisation (Nord/Sud/Sortie).
            parking_objet (ParcDeStationnement): Référence vers le métier.
            base_clients (GestionnaireClients): Référence vers la base de données.
        """
        self.nom = nom_borne
        self.secteur = secteur
        self.parking = parking_objet
        self.clients = base_clients
        self.camera = Camera()
        self.automate = Teleporteur()
        self.distributeur = BorneTicket()

    def traiter_vehicule(self, plaque_immat):
        """
        Gère le flux complet d'entrée d'un véhicule.
        
        Vérifie le format de plaque, identifie le client, mesure le gabarit,
        propose des offres/services et attribue une place.

        Args:
            plaque_immat (str): La plaque saisie ou scannée.

        Returns:
            str: L'identifiant de la place attribuée ou un code d'erreur/redirection.
        """
        if not bool(re.match(r"^[A-Z]{2}[0-9]{4}$", plaque_immat)):
            return "ERREUR_PLAQUE"

        # Simulation Camera
        self.camera.scanner_plaque(plaque_immat)

        # Identification
        usager = self.clients.rechercher_par_plaque(plaque_immat)
        if not usager:
            nom = sd.askstring("Nouveau Client", "Nom de l'usager :")
            if not nom: return None
            usager = Client(nom, plaque_immat)
            self.clients.ajouter_client(usager)
            messagebox.showinfo("Bienvenue", f"Ravi de vous rencontrer {nom} !")
        else:
            messagebox.showinfo("Reconnaissance", f"Content de vous revoir {usager.nom} !")

        # Mesure Gabarit
        try:
            h = sd.askfloat("Capteurs Laser", "Hauteur détectée (m) :", minvalue=1.0, maxvalue=3.0)
            l = sd.askfloat("Capteurs Laser", "Longueur détectée (m) :", minvalue=2.0, maxvalue=6.0)
            if h is None: return None
        except: return None

        # Attribution de place
        res = self.parking.trouver_une_place(h, l, self.secteur, usager.type_offre == "Pack Garanti")
        
        if res == "ORIENTATION_EXTERIEURE": return "PARTENAIRE"
        if res is None: return "PLEIN"

        # --- GESTION DES SERVICES SELON LE STATUT ---
        
        # 1. Si Standard, on propose l'abonnement
        if usager.type_offre == "Standard":
            if messagebox.askyesno("Offre Spéciale", "Voulez-vous devenir 'Abonné' ?"):
                usager.souscrire_offre("Abonné")
                # On propose le Pack Garanti juste après
                if messagebox.askyesno("VIP", "Voulez-vous l'option 'Pack Garanti' (Place assurée même si plein) ?"):
                    usager.souscrire_offre("Pack Garanti")
                self.clients.sauvegarder_donnees()

        # 2. Si le client est éligible, on propose les services
        if usager.type_offre in ["Abonné", "Pack Garanti"]:
            while messagebox.askyesno("Services", "Souhaitez-vous ajouter un service ?"):
                choix = sd.askstring("Catalogue Services", 
                    "Choisissez un service :\n1. Lavage\n2. Maintenance\n3. Livraison")
                
                if choix in ["1", "Lavage"]:
                    usager.services_actifs.append("Lavage")
                elif choix in ["2", "Maintenance"]:
                    usager.services_actifs.append("Maintenance")
                elif choix in ["3", "Livraison"]:
                    dest = sd.askstring("Livraison", "Adresse de destination :")
                    usager.services_actifs.append(f"Livraison ({dest})")
                
                self.clients.sauvegarder_donnees()
                messagebox.showinfo("Panier", f"Services : {', '.join(usager.services_actifs)}")

        # Finalisation matériel
        messagebox.showinfo("Automate", self.automate.deplacer_vers(res.identifiant))
        return res.identifiant

    def gerer_fin_stationnement(self, plaque):
        """
        Gère les notifications de sortie et affiche le détail des services,
        incluant l'adresse de livraison saisie par le client.
        """
        usager = self.clients.rechercher_par_plaque(plaque)
        if not usager: return

        # 1. Notifications services (avec l'adresse de livraison si choisie)
        if usager.services_actifs:
            message_final = f"Rapport de services pour {usager.nom} :\n"
            for s in usager.services_actifs:
                if "Lavage" in s or "Maintenance" in s:
                    message_final += f"- Le service [{s}] a été effectué.\n"
                elif "Livraison" in s:
                    # Ici, 's' contient déjà "Livraison (Adresse)", donc on l'affiche tel quel
                    message_final += f"- Votre véhicule est en route : {s}.\n"
            messagebox.showinfo("Services Effectués", message_final)

        # 2. Gestion Pack Garanti / VIP
        if usager.type_offre == "Pack Garanti":
            rep = messagebox.askyesno("Contrat", "Rester en Pack Garanti (VIP) ?")
            if not rep:
                usager.souscrire_offre("Standard")
        
        # 3. Message matériel
        messagebox.showinfo("Automate", "Le téléporteur ramène votre véhicule vers la sortie...")
        
        # 4. Nettoyage et sauvegarde
        usager.services_actifs = []
        self.clients.sauvegarder_donnees()