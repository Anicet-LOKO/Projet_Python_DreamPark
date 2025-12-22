"""
Module : infrastructure.py
Description : Borne interactive avec reconnaissance et flux logique strict.
"""
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
        # --- VERROU 1 : FORMAT ---
        if not self.valider_format_plaque(plaque_immat):
            print(f"\n[REFUS] Plaque '{plaque_immat}' incorrecte (Format attendu: AA1234).")
            return None

        # --- VERROU 2 : RECONNAISSANCE CLIENT ---
        usager = self.clients.rechercher_par_plaque(plaque_immat)
        if usager:
            print(f"\n[BIENVENUE] Ravi de vous revoir {usager.nom} !")
        else:
            print("\n[NOUVEAU CLIENT] Création de votre profil.")
            nom = input("  > Votre nom : ")
            usager = Client(nom, plaque_immat)
            self.clients.ajouter_client(usager)

        # --- VERROU 3 : GABARIT ---
        h_max_p = max(p.hauteur_maximale for p in self.parking.inventaire_places)
        try:
            h = float(input(f"  > Hauteur (Max {h_max_p}m) : "))
            l = float(input("  > Longueur : "))
            if h > h_max_p:
                print("[REFUS] Gabarit trop haut pour ce parking.")
                return None
        except ValueError: return None

        # --- VERROU 4 : TEST DE DISPONIBILITÉ (AVANT SERVICES) ---
        priorite = usager.verifier_priorite()
        res_place = self.parking.trouver_une_place(h, l, self.secteur, priorite)

        # Cas Parking Plein pour client Standard
        if res_place is None:
            print("\n[PANNEAU] DÉSOLÉ : Parking complet (Nord & Sud).")
            return None

        # Cas Redirection VIP
        if res_place == "ORIENTATION_EXTERIEURE":
            print("\n[INFO] Parking Complet. Redirection Partenaire activée (Pack Garanti).")
            return "PARTENAIRE"

        # Cas Redirection de zone (N vers S ou S vers N)
        if res_place.zone_geographique != self.secteur:
            print(f"\n[INFO] Zone {self.secteur} saturée. Dirigez-vous vers la ZONE {res_place.zone_geographique}.")

        # --- SI PLACE OBTENUE : PROPOSITION DE SERVICES ---
        print(f"\n--- CONFIGURATION DE VOTRE PLACE ({res_place.identifiant}) ---")
        
        # Proposer abonnement si Standard
        if usager.type_offre == "Standard":
            if input("  > Activer le 'Pack Garanti' pour l'avenir ? (o/n) : ").lower() == 'o':
                usager.souscrire_offre("Pack Garanti")

        # Menu Services
        if input("  > Souhaitez-vous des services additionnels ? (o/n) : ").lower() == 'o':
            while True:
                print("    1. Lavage | 2. Pression | 3. Livraison | 4. Terminer")
                c = input("    Choix : ")
                if c == "1": usager.services_actifs.append("Lavage")
                elif c == "2": usager.services_actifs.append("Pression")
                elif c == "3": usager.services_actifs.append("Livraison")
                elif c == "4": break

        print(f"\n[ACTION] Téléportage vers {res_place.identifiant} en cours...")
        return res_place.identifiant