import unittest
import sys
import os
import datetime

# Ajout du dossier parent au système de recherche pour importer les modules racines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Partie4.metier import ParcDeStationnement, PlaceDeParking

class TestMetier(unittest.TestCase):
    def setUp(self):
        """Initialisation : Création d'une instance de parking propre avant chaque test."""
        self.park = ParcDeStationnement("DreamPark")

    def test_initialisation_parking(self):
        """Vérifie que le parking est créé avec 5 places et un CA à zéro."""
        self.assertEqual(len(self.park.inventaire_places), 5)
        self.assertEqual(self.park.compteur_global, 5)
        self.assertEqual(self.park.chiffre_affaire_total, 0.0)

    def test_gabarit_exact_limite(self):
        """Test de la valeur limite : Un véhicule de 2.50m doit être accepté (borne inclusive)."""
        res = self.park.trouver_une_place(2.50, 5.0, "Nord", False)
        self.assertIsNotNone(res, "Le gabarit 2.50m devrait être accepté par l'opérateur >=.")
        self.assertTrue(res.occupee, "La place trouvée doit être marquée comme occupée.")

    def test_gabarit_trop_haut(self):
        """Test d'échec : Un véhicule dépassant la limite (2.51m) doit être refusé."""
        res = self.park.trouver_une_place(2.51, 5.0, "Nord", False)
        self.assertIsNone(res, "Le véhicule est trop haut pour les places de 2.50m.")

    def test_saturation_et_redirection_vip(self):
        """Simule un parking plein et vérifie la redirection spécifique aux clients Pack Garanti."""
        # Saturation manuelle de toutes les places
        for p in self.park.inventaire_places:
            p.occupee = True
        self.park.compteur_global = 0

        # Vérifie que le VIP reçoit le message de redirection
        res_vip = self.park.trouver_une_place(1.8, 4.0, "Nord", True)
        self.assertEqual(res_vip, "ORIENTATION_EXTERIEURE")

        # Vérifie que le client standard est simplement refusé (None)
        res_std = self.park.trouver_une_place(1.8, 4.0, "Nord", False)
        self.assertIsNone(res_std)

    def test_facturation_coherence(self):
        """Vérifie que la libération d'une place calcule un montant et met à jour le CA global."""
        place = self.park.trouver_une_place(1.8, 4.0, "Nord", False)
        # Simulation d'un séjour de 10 minutes en modifiant l'heure d'entrée
        place.heure_entree = datetime.datetime.now() - datetime.timedelta(minutes=10)
        
        ca_initial = self.park.chiffre_affaire_total
        self.park.liberer_une_place(place.identifiant)
        
        # Le chiffre d'affaires doit être strictement supérieur après le départ
        self.assertGreater(self.park.chiffre_affaire_total, ca_initial)
        self.assertFalse(place.occupee, "La place doit être libérée après encaissement.")

if __name__ == '__main__':
    unittest.main()