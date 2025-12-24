from metier import ParcDeStationnement
from infrastructure import BorneDAcces
from gestion_clients import GestionnaireClients

def simulation():
    park = ParcDeStationnement()
    db = GestionnaireClients()
    bornes = {"N": BorneDAcces("B_NORD", "Nord", park, db), "S": BorneDAcces("B_SUD", "Sud", park, db)}
    actifs = {}

    while True:
        print(f"\n--- DREAM PARK v2 (Libre: {park.compteur_global}) ---")
        print("1. Entrée | 2. Sortie | 3. Liste Clients | 4. Stats Finances | 5. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            plaque = input("Plaque (AA1234) : ").upper().strip()
            if plaque in actifs:
                print("Déjà garé.")
                continue
            p = input("Portail (N/S) : ").upper()
            if p in bornes:
                res = bornes[p].traiter_vehicule(plaque)
                if res and res != "PARTENAIRE": actifs[plaque] = res

        elif choix == "2":
            plaque = input("Plaque sortante : ").upper().strip()
            if plaque in actifs:
                if park.liberer_une_place(actifs[plaque]):
                    del actifs[plaque]
            else: print("Véhicule non trouvé.")

        elif choix == "3":
            for p, c in db.annuaire.items():
                print(f"{p} | {c.nom} | {c.type_offre}")

        elif choix == "4":
            print(f"\n[STATS] CA Total : {park.chiffre_affaire_total:.2f} €")
            print(f"[STATS] Occupation : {5 - park.compteur_global}/5 places")

        elif choix == "5":
            break

if __name__ == "__main__":
    simulation()