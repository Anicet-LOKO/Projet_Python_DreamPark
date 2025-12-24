"""
Module métier du système DreamPark.

Ce module définit les classes fondamentales pour la gestion physique du parking,
incluant la configuration des places, les algorithmes de recherche par zone 
et le système de facturation au temps passé.

Auteur : Jean-Claude
"""

import datetime

class PlaceDeParking:
    """
    Représente un emplacement de stationnement individuel.

    Cette classe stocke les dimensions physiques de la place ainsi que 
    son état d'occupation actuel.
    """

    def __init__(self, etiquette, secteur, largeur, hauteur):
        """
        Initialise une place avec ses contraintes de gabarit.

        Args:
            etiquette (str): Identifiant unique de la place (ex: 'NORD-01').
            secteur (str): Zone géographique ('Nord' ou 'Sud').
            largeur (float): Largeur maximale autorisée.
            hauteur (float): Hauteur maximale autorisée.
        """
        self.identifiant = etiquette
        self.zone_geographique = secteur
        self.largeur_maximale = largeur
        self.hauteur_maximale = hauteur
        self.occupee = False
        self.heure_entree = None

class ParcDeStationnement:
    """
    Contrôleur de gestion de l'ensemble des places du parking.

    Gère l'attribution des places en fonction des secteurs d'entrée,
    le suivi du chiffre d'affaires et la libération des emplacements.
    """

    def __init__(self, nom_du_parking="DreamPark"):
        """
        Initialise le parc avec son nom et génère l'inventaire par défaut.
        """
        self.enseigne = nom_du_parking
        self.compteur_global = 5
        self.chiffre_affaire_total = 0.0
        self.inventaire_places = []
        self._remplir_le_parking()

    def _remplir_le_parking(self):
        """
        Génère les places de parking par défaut pour les secteurs Nord et Sud.
        Méthode interne appelée à l'instanciation.
        """
        self.inventaire_places.append(PlaceDeParking("NORD-01", "Nord", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("NORD-02", "Nord", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("SUD-01", "Sud", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("SUD-02", "Sud", 5.0, 2.50))
        self.inventaire_places.append(PlaceDeParking("SUD-03", "Sud", 5.0, 2.50))

    def trouver_une_place(self, h_v, l_v, secteur_entree, est_garanti):
        """
        Recherche une place libre compatible avec le gabarit du véhicule.

        L'algorithme priorise le secteur d'entrée de l'usager avant de 
        basculer sur le secteur opposé si nécessaire.

        Args:
            h_v (float): Hauteur mesurée du véhicule.
            l_v (float): Largeur/Longueur mesurée du véhicule.
            secteur_entree (str): Secteur de la borne d'accès ('Nord' ou 'Sud').
            est_garanti (bool): Statut du client (Pack Garanti).

        Returns:
            PlaceDeParking: L'objet place si trouvé.
            str: "ORIENTATION_EXTERIEURE" si plein et client garanti.
            None: Si aucune solution n'est trouvée pour un client standard.
        """
        zones = [secteur_entree, "Sud" if secteur_entree == "Nord" else "Nord"]
        for z in zones:
            for p in self.inventaire_places:
                if not p.occupee and p.zone_geographique == z:
                    if p.hauteur_maximale >= h_v and p.largeur_maximale >= l_v:
                        p.occupee = True
                        p.heure_entree = datetime.datetime.now()
                        self.compteur_global -= 1
                        return p
        return "ORIENTATION_EXTERIEURE" if est_garanti else None

    def liberer_une_place(self, identifiant_place):
        """
        Libère une place occupée et génère la facturation.

        Le prix est calculé au prorata du temps passé (1.50€ par minute simulée).
        Met à jour le chiffre d'affaires global du parc.

        Args:
            identifiant_place (str): L'étiquette de la place à vider.

        Returns:
            bool: True si la place existait et était occupée, False sinon.
        """
        for p in self.inventaire_places:
            if p.identifiant == identifiant_place and p.occupee:
                duree = datetime.datetime.now() - p.heure_entree
                # Simulation de test : 1 seconde réelle = 1 minute facturée
                minutes = max(1, duree.seconds) 
                montant = minutes * 1.50
                self.chiffre_affaire_total += montant
                p.occupee = False
                p.heure_entree = None
                self.compteur_global += 1
                print(f"\n[FACTURE] Durée : {minutes} min | Montant : {montant:.2f}€")
                return True
        return False