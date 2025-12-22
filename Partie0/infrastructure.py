"""
Module : infrastructure.py
Description : Pilotage des équipements physiques.
Auteur : Jean Claude
"""
import pydoc

class Acces:
    """Point d'entrée/sortie (idAcces, maCamera, maBorne, mesTeleporteurs)."""
    def gerer_entree(self, voiture):
        """Séquence de capture et de validation d'entrée."""
        pass

class Camera:
    """Capteur de mesure (lecture plaque et dimensions)."""
    pass

class BorneTicket:
    """Délivrance et lecture des tickets-paiements."""
    pass

class Teleporteur:
    """Automate de transfert des véhicules."""
    pass

class PanneauAffichage:
    """Afficheur extérieur du nombre de places libres."""
    pass

if __name__ == "__main__":
    pydoc.writedoc("infrastructure")