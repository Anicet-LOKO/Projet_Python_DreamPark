"""
Module : services.py
Description : Services polymorphes pour la Partie 3.
"""

class Service:
    def __init__(self, nom_service, prix):
        self.nom = nom_service
        self.prix = prix

    def appliquer(self):
        """Méthode polymorphe."""
        pass

class Livraison(Service):
    def __init__(self, adresse, heure):
        super().__init__("Livraison Voiturier", 15.0)
        self.adresse = adresse
        self.heure_rdv = heure

    def appliquer(self):
        return f"[SERVICE LIVRAISON] Véhicule sera livré à {self.adresse} vers {self.heure_rdv}."

class Maintenance(Service):
    def __init__(self, type_action):
        super().__init__("Maintenance", 20.0)
        self.type_action = type_action # ex: Lavage, Pression

    def appliquer(self):
        return f"[SERVICE MAINTENANCE] Action : {self.type_action} programmée."