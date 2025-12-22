"""
Module : main_partie1.py
Description : Contrôleur de simulation pour tester la saturation et la reconnaissance.
"""
from metier import ParcDeStationnement
from infrastructure import BorneDAcces
from gestion_clients import GestionnaireClients

def simulation_finale():
    # Initialisation
    park = ParcDeStationnement()
    db = GestionnaireClients()
    
    # Nos deux bornes d'entrée
    bornes = {
        "N": BorneDAcces("PORTAIL_NORD", "Nord", park, db),
        "S": BorneDAcces("PORTAIL_SUD", "Sud", park, db)
    }
    
    # Registre des voitures actuellement garées dans le parking
    # Format : { "PLAQUE": "ID_PLACE" }
    voitures_garees = {}

    while True:
        print(f"\n" + "="*50)
        print(f" ÉTAT DU PARKING : {park.compteur_global}/5 PLACES LIBRES")
        print("="*50)
        print("1. Arrivée d'un véhicule")
        print("2. Sortie d'un véhicule")
        print("3. Consulter la base clients (Annuaire)")
        print("4. Quitter la simulation")
        
        choix = input("\nVotre choix : ")

        if choix == "1":
            plaque = input("Entrez la plaque (ex: AB1234) : ").upper().strip()
            
            # --- VERROU DOUBLON ---
            if plaque in voitures_garees:
                print(f"\n[BLOCAGE] La voiture {plaque} est déjà à la place {voitures_garees[plaque]} !")
                continue
            
            # --- CHOIX DU PORTAIL ---
            p_entree = input("Portail d'entrée (N/S) : ").upper().strip()
            if p_entree in bornes:
                # On lance la borne (Validation -> Gabarit -> Place -> Services)
                resultat = bornes[p_entree].traiter_vehicule(plaque)
                
                # Si le résultat est un ID de place (ex: NORD-01), on enregistre l'entrée
                if resultat and resultat != "PARTENAIRE":
                    voitures_garees[plaque] = resultat
            else:
                print("[ERREUR] Portail inconnu (tapez N ou S).")

        elif choix == "2":
            if not voitures_garees:
                print("\n[INFO] Le parking est vide.")
                continue
            
            print("\nVéhicules présents :", list(voitures_garees.keys()))
            plaque_out = input("Plaque du véhicule qui sort : ").upper().strip()
            
            if plaque_out in voitures_garees:
                id_place = voitures_garees[plaque_out]
                if park.liberer_une_place(id_place):
                    del voitures_garees[plaque_out]
                    print(f"[SORTIE] Véhicule {plaque_out} libéré.")
            else:
                print("[ERREUR] Ce véhicule n'est pas dans le parking.")

        elif choix == "3":
            print("\n" + "-"*30)
            print("REGISTRE DES CLIENTS ENREGISTRÉS")
            print("-"*30)
            if not db.annuaire:
                print("Aucun client en base.")
            for p, c in db.annuaire.items():
                statut = f"Garé ({voitures_garees[p]})" if p in voitures_garees else "Absent"
                services = ", ".join(c.services_actifs) if c.services_actifs else "Aucun"
                print(f"Plaque: {p} | Nom: {c.nom:10} | Offre: {c.type_offre:12} | Statut: {statut}")
                print(f"   > Services consommés : {services}")

        elif choix == "4":
            print("Fin du programme.")
            break

if __name__ == "__main__":
    simulation_finale()