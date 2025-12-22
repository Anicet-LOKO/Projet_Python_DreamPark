import pydoc
""" la classe client represente un client du parking
"""
class client(object):
    
    """definition de la methode init avec les coordonées du client"""
    def __init__(self, nom, adresse, estabonne, estSuperAbonné, nbrFrequentation):
        """
        param nom= nom du client
        param adresse= adresse du client
        param estAbonne= statutrenvoie un booleen true ou false sur le statut abonné du client
        param estSuperAbonne= renvoie un booleen true ou falase sur le statu superAbonné du client 
        param nbFréquentation= prends en compte l'affluence du client au parking """
        self.nom= nom
        self.adresse= adresse
        self.estabonne= estabonne
        self.estSuperAbonne=estSuperAbonné
        self.nbFrequentation= nbrFrequentation

    def sAbonner(self):
        """
        methode qui propose à un client quelconque de s'abonner
        """
    def nouvelleVoiture(self, imma, hautV, longV):
        """ 
        methode pour enregistrer une nouvelle voiture d'un nouveau client

        param imma= n° matricule de la voiture
        param hautV= enregistre la hauteur de la voiture
        param longV= enregistre la longueur de la voiture
        """

pydoc.writedoc('doc')

"""
Auteur: Anicet Darcia NKOUNKOU LOKO & Jean Claude KARANGANWA
Date d'emission: 
"""