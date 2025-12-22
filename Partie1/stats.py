"""
Module : stats.py (Dossier Partie 1)
Description : Enregistrement des flux d'entrée/sortie.
Auteur : Anicet-Darcia
"""
import pydoc
from datetime import datetime

class Historique:
    def __init__(self):
        self.logs = []

    def enregistrer(self, immatriculation, action, place_id):
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entree = f"[{horodatage}] {action} | Véhicule: {immatriculation} | Place: {place_id}"
        self.logs.append(entree)
        print(f"Log : {entree}")

if __name__ == "__main__":
    h = Historique()
    h.enregistrer("AB-123-CD", "ENTREE", "L3-42")