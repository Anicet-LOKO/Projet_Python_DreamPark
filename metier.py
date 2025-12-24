import datetime

class PlaceDeParking:
    def __init__(self, etiquette, secteur, largeur, hauteur):
        self.identifiant = etiquette
        self.zone_geographique = secteur
        self.largeur_maximale = largeur
        self.hauteur_maximale = hauteur
        self.occupee = False
        self.heure_entree = None

class ParcDeStationnement:
    def __init__(self, nom_du_parking="DreamPark"):
        self.enseigne = nom_du_parking
        self.compteur_global = 5
        self.chiffre_affaire_total = 0.0
        self.inventaire_places = []
        self._remplir_le_parking()

    def _remplir_le_parking(self):
        self.inventaire_places.append(PlaceDeParking("NORD-01", "Nord", 5.0, 1.90))
        self.inventaire_places.append(PlaceDeParking("NORD-02", "Nord", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("SUD-01", "Sud", 5.0, 1.90))
        self.inventaire_places.append(PlaceDeParking("SUD-02", "Sud", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("SUD-03", "Sud", 5.0, 1.90))

    def trouver_une_place(self, h_v, l_v, secteur_entree, est_garanti):
        # Recherche en zone d'entrée puis alternative
        zones_priorite = [secteur_entree, "Sud" if secteur_entree == "Nord" else "Nord"]
        for z in zones_priorite:
            for p in self.inventaire_places:
                if not p.occupee and p.zone_geographique == z:
                    if p.hauteur_maximale >= h_v and p.largeur_maximale >= l_v:
                        p.occupee = True
                        p.heure_entree = datetime.datetime.now()
                        self.compteur_global -= 1
                        return p
        return "ORIENTATION_EXTERIEURE" if est_garanti else None

    def liberer_une_place(self, identifiant_place):
        for p in self.inventaire_places:
            if p.identifiant == identifiant_place and p.occupee:
                # Calcul : 1 seconde réelle = 1 minute de parking (Tarif : 1.50€ / min)
                duree = datetime.datetime.now() - p.heure_entree
                minutes = max(1, duree.seconds) 
                montant = minutes * 1.50
                
                self.chiffre_affaire_total += montant
                p.occupee = False
                p.heure_entree = None
                self.compteur_global += 1
                print(f"\n  [FACTURE] Durée : {minutes} min | TOTAL : {montant:.2f}€")
                return True
        return False