"""
Module : services.py (Dossier Partie 1)
Description : Services de maintenance et livraison pour abonnés.
Auteur : Jean Claude
"""
import pydoc

class Service:
    def __init__(self, nom_service, prix):
        self.nom = nom_service
        self.prix = prix
        self.termine = False

class Livraison(Service):
    """Service de voiturier à domicile."""
    def __init__(self, adresse, heure):
        super().__init__("Livraison Voiturier", 15.0)
        self.adresse = adresse
        self.heure_rdv = heure

    def executer(self):
        print(f"Service : Livraison en cours vers {self.adresse} à {self.heure_rdv}.")
        self.termine = True

if __name__ == "__main__":
    test_livraison = Livraison("12 rue de la Paix", "18:00")
    test_livraison.executer()