import re
from gestion_clients import Client

class BorneDAcces:
    def __init__(self, nom_borne, secteur, parking_objet, base_clients):
        self.nom = nom_borne
        self.secteur = secteur
        self.parking = parking_objet
        self.clients = base_clients

    def valider_format_plaque(self, plaque):
        return bool(re.match(r"^[A-Z]{2}[0-9]{4}$", plaque))

    def traiter_vehicule(self, plaque_immat):
        if not self.valider_format_plaque(plaque_immat):
            print(f"\n[ERREUR] Plaque '{plaque_immat}' invalide.")
            return None

        usager = self.clients.rechercher_par_plaque(plaque_immat)
        if usager:
            print(f"\n[RECONNAISSANCE] Bonjour {usager.nom} !")
        else:
            nom = input("\n[NOUVEAU] Entrez votre nom : ")
            usager = Client(nom, plaque_immat)
            self.clients.ajouter_client(usager)

        try:
            h = float(input("  > Hauteur véhicule : "))
            l = float(input("  > Longueur véhicule : "))
        except ValueError: return None

        res = self.parking.trouver_une_place(h, l, self.secteur, usager.verifier_priorite())

        if res is None:
            print("\n[INFO] Parking Complet.")
            return None
        elif res == "ORIENTATION_EXTERIEURE":
            print("\n[VIP] Redirection Partenaire.")
            return "PARTENAIRE"

        print(f"\n[OK] Place {res.identifiant} attribuée.")
        return res.identifiant