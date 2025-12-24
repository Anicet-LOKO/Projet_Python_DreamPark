import tkinter as tk
from metier import ParcDeStationnement
from gestion_clients import GestionnaireClients
from gui import DreamParkGUI

def main():
    # 1. Préparation du métier
    park = ParcDeStationnement("DreamPark L3 MIASHS")
    db = GestionnaireClients()

    # 2. Lancement de la fenêtre
    root = tk.Tk()
    app = DreamParkGUI(root, park, db)
    
    root.mainloop()

if __name__ == "__main__":
    main()