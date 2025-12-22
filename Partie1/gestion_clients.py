"""
Module : gestion_clients.py
Description : Gestion des usagers et de l'unicité des plaques.
"""

class Client:
    def __init__(self, nom, plaque, offre="Standard"):
        self.nom = nom
        self.plaque_immatriculation = plaque
        self.type_offre = offre
        self.services_actifs = []

    def verifier_priorite(self):
        return self.type_offre == "Pack Garanti"

    def souscrire_offre(self, nouvelle_offre):
        self.type_offre = nouvelle_offre
        print(f"  [CONTRAT] : {self.nom} est passé en offre {nouvelle_offre}.")

class GestionnaireClients:
    def __init__(self):
        self.annuaire = {}

    def ajouter_client(self, client):
        # Unicité : On vérifie si la plaque appartient déjà à quelqu'un d'autre
        if client.plaque_immatriculation in self.annuaire:
            existant = self.annuaire[client.plaque_immatriculation]
            if existant.nom != client.nom:
                print(f"  [ERREUR] : La plaque {client.plaque_immatriculation} est déjà enregistrée au nom de {existant.nom}!")
                return False
        self.annuaire[client.plaque_immatriculation] = client
        return True

    def rechercher_par_plaque(self, plaque):
        return self.annuaire.get(plaque)