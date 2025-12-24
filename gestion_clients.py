"""
Module de gestion de la base de données clients du DreamPark.

Ce module assure le suivi des usagers et la persistance des données 
via un système de sérialisation JSON.

Auteur : Jean-Claude
"""

import json

class Client:
    """
    Représente un usager du parking et ses caractéristiques.

    Cette classe stocke l'identité du client, son véhicule ainsi que 
    son niveau d'abonnement pour l'accès aux services.
    """

    def __init__(self, nom, plaque, offre="Standard"):
        """
        Initialise un nouveau profil client.

        Args:
            nom (str): Nom et prénom de l'usager.
            plaque (str): Plaque d'immatriculation servant d'identifiant unique.
            offre (str): Type de contrat ('Standard', 'Abonné', 'Pack Garanti').
        """
        self.nom = nom
        self.plaque_immatriculation = plaque
        self.type_offre = offre
        self.services_actifs = [] # Liste pour le polymorphisme

    def souscrire_offre(self, nouvelle_offre):
        """
        Met à jour le statut contractuel du client.

        Args:
            nouvelle_offre (str): Le nouvel intitulé de l'offre choisie.
        """
        self.type_offre = nouvelle_offre

class GestionnaireClients:
    """
    Système de gestion de l'annuaire et de la persistance.

    Cette classe fait le pont entre les objets Python en mémoire et 
    le stockage physique dans un fichier JSON.
    """

    def __init__(self):
        """
        Initialise le gestionnaire et charge automatiquement les données existantes.
        """
        self.annuaire = {}
        self.fichier_db = "base_clients.json"
        self.charger_donnees()

    def ajouter_client(self, client):
        """
        Inscrit un nouveau client dans l'annuaire et synchronise le fichier JSON.

        Args:
            client (Client): L'objet client à enregistrer.

        Returns:
            bool: True après confirmation de l'ajout.
        """
        self.annuaire[client.plaque_immatriculation] = client
        self.sauvegarder_donnees()
        return True

    def rechercher_par_plaque(self, plaque):
        """
        Recherche un client dans l'annuaire à partir de sa plaque.

        Args:
            plaque (str): La plaque à rechercher.

        Returns:
            Client: L'objet client si trouvé, None sinon.
        """
        return self.annuaire.get(plaque)

    def sauvegarder_donnees(self):
        """
        Sérialise l'annuaire actuel au format JSON dans le fichier de base de données.
        """
        with open(self.fichier_db, "w", encoding="utf-8") as f:
            data = {p: {"nom": c.nom, "offre": c.type_offre} for p, c in self.annuaire.items()}
            json.dump(data, f, indent=4)

    def charger_donnees(self):
        """
        Désérialise les données du fichier JSON pour reconstruire les objets Client en mémoire.
        Gère l'absence de fichier au premier lancement.
        """
        try:
            with open(self.fichier_db, "r", encoding="utf-8") as f:
                data = json.load(f)
                for p, info in data.items():
                    self.annuaire[p] = Client(info["nom"], p, info["offre"])
        except FileNotFoundError: pass