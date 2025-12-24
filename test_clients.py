import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Partie4.gestion_clients import GestionnaireClients, Client

class TestClients(unittest.TestCase):
    def setUp(self):
        """Prépare un gestionnaire de clients vide pour isoler les tests."""
        self.gestion = GestionnaireClients()
        self.gestion.annuaire = {} 

    def test_creation_et_attributs(self):
        """Vérifie que l'objet Client stocke correctement les informations et l'offre par défaut."""
        c = Client("Anicet", "ABC-123")
        self.assertEqual(c.nom, "Anicet")
        self.assertEqual(c.type_offre, "Standard") # Vérification de la valeur initiale
        self.assertNotEqual(c.type_offre, "Pack Garanti")

    def test_abonnement_vip(self):
        """Vérifie que la méthode souscrire_offre change correctement le statut du client."""
        c = Client("Jean-Claude", "XYZ-999")
        c.souscrire_offre("Pack Garanti")
        self.assertEqual(c.type_offre, "Pack Garanti")

    def test_recherche_client_inexistant(self):
        """Vérifie que le système gère les plaques d'immatriculation inconnues sans erreur."""
        res = self.gestion.rechercher_par_plaque("INTROUVABLE")
        self.assertIsNone(res, "La recherche doit renvoyer None pour une plaque inexistante.")
    
    def test_sauvegarde_et_chargement_json(self):
        """Vérifie que les données persistent après une sauvegarde."""
        nom_test = "Client_Test_Persistence"
        plaque_test = "ZZ9999"
        
        # 1. Création et sauvegarde
        nouveau_client = Client(nom_test, plaque_test)
        self.gestion.ajouter_client(nouveau_client)
        self.gestion.sauvegarder_donnees()
        
        # 2. On simule un rechargement (en créant une nouvelle instance)
        nouvelle_gestion = GestionnaireClients() 
        # On suppose que le constructeur fait un charger_donnees()
        
        client_recupere = nouvelle_gestion.rechercher_par_plaque(plaque_test)
        
        self.assertIsNotNone(client_recupere, "Le client devrait être retrouvé dans le fichier JSON")
        self.assertEqual(client_recupere.nom, nom_test)

    def test_validation_plaque_regex(self):
        """Vérifie si la logique de plaque (dans infrastructure.py de la partie4) est cohérente."""
        import re
        pattern = r"^[A-Z]{2}[0-9]{4}$"
        self.assertTrue(bool(re.match(pattern, "AA1234")))
        self.assertFalse(bool(re.match(pattern, "ABC-1234"))) # Trop de chiffres/lettres

if __name__ == '__main__':
    unittest.main()