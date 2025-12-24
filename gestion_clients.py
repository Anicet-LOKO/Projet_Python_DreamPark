import json

class Client:
    def __init__(self, nom, plaque, offre="Standard"):
        self.nom = nom
        self.plaque_immatriculation = plaque
        self.type_offre = offre
        self.services_actifs = [] # Liste pour le polymorphisme

    def souscrire_offre(self, nouvelle_offre):
        self.type_offre = nouvelle_offre

class GestionnaireClients:
    def __init__(self):
        self.annuaire = {}
        self.fichier_db = "base_clients.json"
        self.charger_donnees()

    def ajouter_client(self, client):
        self.annuaire[client.plaque_immatriculation] = client
        self.sauvegarder_donnees()
        return True

    def rechercher_par_plaque(self, plaque):
        return self.annuaire.get(plaque)

    def sauvegarder_donnees(self):
        with open(self.fichier_db, "w", encoding="utf-8") as f:
            data = {p: {"nom": c.nom, "offre": c.type_offre} for p, c in self.annuaire.items()}
            json.dump(data, f, indent=4)

    def charger_donnees(self):
        try:
            with open(self.fichier_db, "r", encoding="utf-8") as f:
                data = json.load(f)
                for p, info in data.items():
                    self.annuaire[p] = Client(info["nom"], p, info["offre"])
        except FileNotFoundError: pass