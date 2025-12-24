import re
from gestion_clients import Client
from services import Livraison, Maintenance

class BorneDAcces:
    def __init__(self, nom_borne, secteur, parking_objet, base_clients):
        self.nom = nom_borne
        self.secteur = secteur
        self.parking = parking_objet
        self.clients = base_clients

    def traiter_vehicule(self, plaque):
        if not re.match(r"^[A-Z]{2}[0-9]{4}$", plaque):
            print("[ERREUR] Format plaque invalide.")
            return None

        usager = self.clients.rechercher_par_plaque(plaque)
        if not usager:
            nom = input("Nouveau ! Votre nom : ")
            usager = Client(nom, plaque)
            self.clients.ajouter_client(usager)

        h = float(input("Hauteur (m) : "))
        l = float(input("Longueur (m) : "))
        
        res = self.parking.trouver_une_place(h, l, self.secteur, usager.type_offre == "Pack Garanti")
        
        if res == "ORIENTATION_EXTERIEURE":
            print("[VIP] Parking complet, redirigé vers partenaire.")
            return "PARTENAIRE"
            
        if res:
            print(f"BIENVENU {usager.nom} -> Place {res.identifiant}")
            # Simulation Services Polymorphes
            if input("Service ? (o/n) : ") == 'o':
                c = input("1. Livraison | 2. Maintenance : ")
                s = Livraison("Avenue Foch", "20h") if c=="1" else Maintenance("Lavage")
                usager.services_actifs.append(s)
                print(s.appliquer()) # Polymorphisme ici
            return res.identifiant
        return None