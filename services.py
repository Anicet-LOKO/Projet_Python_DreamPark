"""
Module des services polymorphes du DreamPark.

Ce module définit la structure des prestations additionnelles proposées aux clients.
Il utilise le concept d'héritage et de polymorphisme pour permettre l'extension
facile du catalogue de services (Lavage, Livraison, etc.).

Auteur : Anicet-Darcia
"""

class Service:
    """
    Classe de base abstraite pour tous les services du parking.

    Attributs:
        nom (str): Désignation commerciale du service.
        prix (float): Tarif forfaitaire du service.
    """
    def __init__(self, nom_service, prix):
        """Initialise les propriétés communes à tous les services."""
        self.nom = nom_service
        self.prix = prix

    def appliquer(self):
        """
        Méthode polymorphe devant être surchargée par les classes filles.
        Définit l'action concrète à réaliser pour le service.
        """
        pass

class Livraison(Service):
    """
    Service de livraison du véhicule par un voiturier.

    Permet de restituer le véhicule à une adresse précise plutôt que 
    sur le lieu de stationnement initial.
    """
    def __init__(self, adresse, heure):
        """
        Initialise une demande de livraison.

        Args:
            adresse (str): Destination de livraison.
            heure (str): Créneau horaire souhaité pour le rendez-vous.
        """
        super().__init__("Livraison Voiturier", 15.0)
        self.adresse = adresse
        self.heure_rdv = heure

    def appliquer(self):
        """Retourne les détails logistiques de la livraison."""
        return f"[SERVICE LIVRAISON] Véhicule sera livré à {self.adresse} vers {self.heure_rdv}."

class Maintenance(Service):
    """
    Service d'entretien technique du véhicule.

    Regroupe les actions de nettoyage, de vérification des niveaux ou de pression.
    """
    def __init__(self, type_action):
        """
        Initialise une action de maintenance.

        Args:
            type_action (str): Nature de l'intervention (ex: 'Lavage', 'Pression').
        """
        super().__init__("Maintenance", 20.0)
        self.type_action = type_action 

    def appliquer(self):
        """Retourne la confirmation de l'action de maintenance programmée."""
        return f"[SERVICE MAINTENANCE] Action : {self.type_action} programmée."