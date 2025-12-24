import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Partie4.services import Livraison, Maintenance, Service

class TestServices(unittest.TestCase):
    def test_heritage_et_prix(self):
        """Vérifie que Livraison et Maintenance héritent bien de la classe Service (Polymorphisme)."""
        L = Livraison("Mairie de Paris", "12h00")
        M = Maintenance("Lavage")
        
        # Test de type : vérifie la structure de classe
        self.assertIsInstance(L, Service)
        self.assertIsInstance(M, Service)
        # Vérifie que les prix sont bien assignés via super().__init__
        self.assertEqual(L.prix, 15.0)
        self.assertEqual(M.prix, 20.0)

    def test_contenu_message_livraison(self):
        """Vérifie que la méthode appliquer() de Livraison retourne les bonnes informations."""
        adresse = "10 Rue des Fleurs"
        s = Livraison(adresse, "08h00")
        msg = s.appliquer()
        
        # Vérifie le formatage du message
        self.assertTrue(msg.startswith("[SERVICE LIVRAISON]"))
        self.assertIn(adresse, msg)

    def test_contenu_message_maintenance(self):
        """Vérifie que la méthode appliquer() de Maintenance mentionne bien l'action choisie."""
        action = "Pression des pneus"
        s = Maintenance(action)
        msg = s.appliquer()
        
        self.assertIn(action, msg)
        self.assertIn("programmée", msg)

if __name__ == '__main__':
    unittest.main()