"""
Module : main_partie3.py
Description : Contrôleur détaillé intégrant le polymorphisme et la gestion financière.
"""
from metier import ParcDeStationnement
from infrastructure import BorneDAcces
from gestion_clients import GestionnaireClients

def simulation_detaillee():
    # 1. Initialisation des composants coeurs
    park = ParcDeStationnement()
    db = GestionnaireClients()
    
    # 2. Configuration des bornes (Nord et Sud)
    bornes = {
        "N": BorneDAcces("B_NORD", "Nord", park, db),
        "S": BorneDAcces("B_SUD", "Sud", park, db)
    }
    
    # 3. Registre local pour le suivi des véhicules en cours de stationnement
    # Clé : Plaque | Valeur : ID_Place
    actifs = {}

    while True:
        print("\n" + "="*60)
        print(f" DREAMPARK P3 - GESTIONNAIRE DE FLUX (Libre: {park.compteur_global}/5)")
        print("="*60)
        print("1. Arrivée (Portail)")
        print("2. Sortie (Facturation)")
        print("3. Registre des Clients (Services & Offres)")
        print("4. Bilan Financier (CA)")
        print("5. Quitter")
        print("-"*60)
        
        choix = input("Sélectionnez une option : ")

        if choix == "1":
            print("\n--- PROCÉDURE D'ENTRÉE ---")
            plaque = input("Lecture Caméra (Plaque AA1234) : ").upper().strip()
            
            # Vérification si déjà dans le parking
            if plaque in actifs:
                print(f"[ALERTE] Le véhicule {plaque} est déjà enregistré à la place {actifs[plaque]}.")
                continue
                
            p = input("Portail d'entrée (N/S) : ").upper()
            if p in bornes:
                # La borne gère la reconnaissance, le gabarit et les services polymorphes
                res = bornes[p].traiter_vehicule(plaque)
                
                if res and res != "PARTENAIRE":
                    actifs[plaque] = res
                    print(f"[OK] Accès autorisé. Ticket généré pour la place {res}.")
            else:
                print("[ERREUR] Portail inconnu.")

        elif choix == "2":
            print("\n--- PROCÉDURE DE SORTIE ---")
            if not actifs:
                print("[INFO] Aucun véhicule à libérer.")
                continue
                
            print(f"Véhicules présents : {list(actifs.keys())}")
            plaque_out = input("Plaque du véhicule sortant : ").upper().strip()
            
            if plaque_out in actifs:
                id_place = actifs[plaque_out]
                # liberer_une_place calcule le montant basé sur le temps réel
                if park.liberer_une_place(id_place):
                    del actifs[plaque_out]
                    print(f"[SORTIE] Place {id_place} maintenant vacante.")
            else:
                print("[ERREUR] Véhicule introuvable dans le registre actif.")

        elif choix == "3":
            print("\n" + "-"*60)
            print(f"{'PLAQUE':<10} | {'NOM':<12} | {'OFFRE':<12} | {'SERVICES'}")
            print("-"*60)
            if not db.annuaire:
                print("Aucun client enregistré dans base_clients.json.")
            else:
                for p, c in db.annuaire.items():
                    # Affichage du polymorphisme : on liste les services s'ils existent
                    liste_serv = ", ".join([s.nom for s in c.services_actifs]) if c.services_actifs else "Aucun"
                    statut = f"({actifs[p]})" if p in actifs else ""
                    print(f"{p:<10} | {c.nom:<12} | {c.type_offre:<12} | {liste_serv} {statut}")

        elif choix == "4":
            print("\n" + "*"*30)
            print(f" BILAN CHIFFRE D'AFFAIRES ")
            print(f" Total perçu : {park.chiffre_affaire_total:.2f} €")
            print("*"*30)

        elif choix == "5":
            print("Fermeture du système DreamPark. Sauvegarde des données...")
            break

if __name__ == "__main__":
    simulation_detaillee()