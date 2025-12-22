"""
Module : services.py
Description : Services exclusifs aux abonnés.
Auteur : Jean Claude
"""
import pydoc

class Service:
    """Classe mère des prestations (dateDemande, estRealise)."""
    pass

class Livraison(Service):
    """Vérifier que le client est éligible avant de programmer le voiturier."""
    def programmer_livraison(self, adresse, heure):
        """Test : Empêcher la programmation si le véhicule est hors parking."""
        pass

class Maintenance(Service):
    """Réparations durant le stationnement."""
    pass

class Entretien(Service):
    """Nettoyage et lavage."""
    pass

if __name__ == "__main__":
    pydoc.writedoc("services")