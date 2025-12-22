"""
Module : metier.py
Description : Gestion des places avec basculement automatique entre zones.
"""

class PlaceDeParking:
    def __init__(self, etiquette, secteur, largeur, hauteur):
        self.identifiant = etiquette
        self.zone_geographique = secteur
        self.largeur_maximale = largeur
        self.hauteur_maximale = hauteur
        self.occupee = False

class ParcDeStationnement:
    def __init__(self, nom_du_parking="DreamPark"):
        self.enseigne = nom_du_parking
        self.compteur_global = 5
        self.inventaire_places = []
        self._remplir_le_parking()

    def _remplir_le_parking(self):
        # 3 places au Nord, 2 places au Sud
        self.inventaire_places.append(PlaceDeParking("NORD-01", "Nord", 5.0, 1.90))
        self.inventaire_places.append(PlaceDeParking("NORD-02", "Nord", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("NORD-03", "Nord", 5.0, 1.90))
        self.inventaire_places.append(PlaceDeParking("SUD-01", "Sud", 5.0, 1.90))
        self.inventaire_places.append(PlaceDeParking("SUD-02", "Sud", 5.0, 2.50))

    def trouver_une_place(self, h_v, l_v, secteur_entree, est_garanti):
        # 1. ESSAI DANS LA ZONE DE L'ENTRÉE
        for p in self.inventaire_places:
            if not p.occupee and p.zone_geographique == secteur_entree:
                if p.hauteur_maximale >= h_v and p.largeur_maximale >= l_v:
                    p.occupee = True
                    self.compteur_global -= 1
                    return p
        
        # 2. BASCULEMENT AUTOMATIQUE : Si l'entrée est pleine, on regarde l'autre zone
        autre = "Sud" if secteur_entree == "Nord" else "Nord"
        for p in self.inventaire_places:
            if not p.occupee and p.zone_geographique == autre:
                if p.hauteur_maximale >= h_v and p.largeur_maximale >= l_v:
                    p.occupee = True
                    self.compteur_global -= 1
                    return p
        
        # 3. SI AUCUNE PLACE (NORD + SUD)
        if est_garanti:
            return "ORIENTATION_EXTERIEURE"
        
        return None

    def liberer_une_place(self, identifiant_place):
        for p in self.inventaire_places:
            if p.identifiant == identifiant_place and p.occupee:
                p.occupee = False
                self.compteur_global += 1
                print(f"  [SYSTÈME] : Place {identifiant_place} libérée. Reste : {self.compteur_global}")
                return True
        return False