# DreamPark – Partie 0
## 1. Objectif
Mettre en place les spécifications fonctionnelles et les tests pour le système de gestion du parking DreamPark.

## 2. Fonctionnalités
### 2.1 Gestion des places
- Chaque place possède : identifiant unique, niveau, longueur, hauteur.
- La place est assignée automatiquement à une voiture lors de son entrée.
- Libération de la place lors de la sortie du véhicule.

### 2.2 Entrée et sortie des véhicules
- Deux accès équipés de caméras et bornes à tickets.
- Capturer l’immatriculation, la longueur et la hauteur du véhicule.
- Affichage du nombre de places disponibles sur panneaux.

### 2.3 Services
- Livraison de véhicules par voiturier.
- Stationnement garanti pour abonnés.
- Gestion des abonnements et modes de paiement.

### 2.4 Interactions
- Borne délivre le ticket et pose des questions (abonnement, paiement, options).
- Téléporteurs déplacent le véhicule à la place assignée.
- Mise à jour des panneaux à chaque entrée/sortie.

## 3. Tests (Partie 0)
- **Test 1 : assigner une place si disponible**
- **Test 2 : retour d’erreur si parking plein**
- **Test 3 : vérification des informations d’entrée du véhicule**
- **Test 4 : mise à jour du nombre de places disponibles**
- **Test 5 : prise en charge des services abonnés (livraison, entretien)**

> Ces tests sont **conceptuels** pour la Partie 0 et seront implémentés dans la Partie 1.