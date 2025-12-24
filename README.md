# PROJET DREAM PARK - L3 MIASHS 2024-2025
![Aperçu de l'interface](DreamPark_interface.png)
Bienvenue dans le dépôt du projet DreamPark, une solution logicielle complète de gestion pour un parking automatisé.

## Equipe de Développement
* Jean-Claude KARANGANWA : Responsable partie metier.py, gestion_clients.py.
* Anicet-Darcia NKOUNKOU LOKO : Responsable Interface (infrastructure.py, services.py, gui.py).

## Présentation du Projet
DreamPark est un système de gestion automatisé conçu pour optimiser l'occupation des places et l'expérience client. Le logiciel gère l'entrée/sortie des véhicules, l'attribution intelligente des places par zone et par gabarit, ainsi qu'un catalogue de services additionnels pour les abonnés uniquement.

### Fonctionnalités Cles :
* Statut VIP (Pack Garanti) : Reconnaissance prioritaire, affichage spécifique VIP sur le tableau de bord et garantie de place avec redirection partenaire en cas de saturation.
* Services Polymorphes : Lavage, Maintenance, et Livraison. Le système mémorise les détails spécifiques (ex: adresse de destination) pour le rapport final quand la voiture sort.
* Persistance des données : Sauvegarde automatique et sécurisée des profils clients et des abonnements dans le fichier base_clients.json.
* Traçabilité : Génération d'un rapport de sortie détaillé incluant le récapitulatif des services consommés et la facturation au temps passé.

## Architecture Logicielle
Notre projet repose sur les piliers de la POO :

 * Encapsulation : Les attributs des places et des clients sont protégés et modifiés via des méthodes dédiées (ex: souscrire_offre).
 * Héritage & Polymorphisme : Utilisés dans services.py. Tous les services héritent d'une classe mère Service, permettant de traiter de la même manière une "Maintenance" ou une "Livraison" dans le code
 * Modularité : Le code est divisé en 5 fichiers distincts pour faciliter la maintenance et la lecture.

## Installation et Lancement
1. Prérequis : Python 3.10 ou supérieur installé.
2. Lancement de l'application :
    cd partie4
    python main_partie4.py

## Documentation Technique (Pydoc)
Conformément aux exigences du cours, l'intégralité du code source est documentée selon les standards professionnels Pydoc. Cette documentation inclut les signatures des auteurs ainsi que la description détaillée des classes et des méthodes
pour consulter ouvrez les fichier html présent dans le depot
* commande utilisé pour générer les fichiers: 
python -m pydoc -w metier services gestion_clients infrastructure gui

## Qualité et Tests (Coverage)
Afin de garantir la fiabilité des algorithmes de facturation et de gestion des places, nous avons mis en place une suite de tests unitaires située dans le répertoire /tests.
Nous avons mesuré la couverture de code avec l'outil Coverage.py, atteignant un score de 97%. Le rapport complet est disponible via le fichier .coverage et le rapport visuel HTML.
* commande utilisé: 
python -m coverage run -m unittest discover
python -m coverage html

## Environnement Technique
Langage : Python 3
Interface Graphique : Tkinter
Gestion de Qualité : Coverage.py / Unittest
Format de Données : JSON 
Validation : Expressions régulières (Regex)
Diagramme UML: plantUML:
## Conception et Modélisation

### Diagramme de Classes (Héritage et Structure)
```plantuml
@startuml
skinparam style strict
abstract class Service {
    + nom : str
    + prix_base : float
    + {abstract} calculer_cout()
}
class Lavage extends Service
class Maintenance extends Service
class Livraison extends Service
class ParcDeStationnement {
    + places : list
    + attribuer_place()
}
ParcDeStationnement "1" *-- "many" PlaceDeParking
Client "1" o-- "many" Service
@enduml

## Méthodologie de Collaboration
Bien que l'outil Git n'ait pas été utilisé pour ce projet (pour des raisons techniques), nous avons mis en place une gestion de versions manuelle et une répartition modulaire stricte :
 * Découpage par fichiers : Chaque membre était responsable de fichiers spécifiques afin d'éviter les conflits d'édition (Jean-Claude sur la logique métier, Anicet-Darcia sur l'interface et le matériel et les tests unitaires).
 * Échanges synchronisés : points de contrôle réguliers pour fusionner les différentes parties du code.
 * Revues de code : Chaque module a été relu par l'autre membre du binôme pour assurer la cohérence des noms de variables et la qualité des commentaires Pydoc jusqu'à l'obtention de cette version finale.

 ## Conception et Modélisation
L'architecture logicielle a été définie en amont de la phase de codage afin de respecter les principes:
 * Modèle de données : Utilisation d'un diagramme de classes pour structurer l'héritage des services et la gestion des places.
 * Logique de flux: Analyse des scénarios d'entrée/sortie via des diagrammes de séquence pour garantir la synchronisation entre l'interface et le moteur métier.