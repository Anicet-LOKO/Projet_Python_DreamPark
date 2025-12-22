"""
Module : gestion_clients.py
Description : Gestion des usagers et de leurs droits.
Auteur : Anicet-Darcia
"""
import pydoc

class Client:
    """Usager du parking (nom, estAbonne, monAbonnement)."""
    def s_abonner(self, type_contrat):
        """Passage au statut Abonné ou Pack Garanti."""
        pass

class Voiture:
    """Véhicule associé au client (immatriculation, hauteur, longueur)."""
    pass

class Abonnement:
    """Contrat de service (Simple ou Pack Garanti)."""
    pass

class Contrat:
    """Document de validité (dateSignature)."""
    pass

if __name__ == "__main__":
    pydoc.writedoc("gestion_clients")