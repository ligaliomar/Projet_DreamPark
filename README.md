# README - Projet Parking DreamPark

## Description
Système de gestion de parking développé dans le cadre du projet Python L3 MIASHS.
Le parking DreamPark permet de gérer l'entrée et la sortie des véhicules, avec un système d'abonnement.

## Installation

1. Cloner le projet
2. Créer un environnement virtuel :
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Installer Django :
```bash
pip install django
```

4. Faire les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Lancer le serveur :
```bash
python manage.py runserver
```

## Fonctionnalités implémentées

### ✅ Obligatoires
- **Modèles** : Vehicle, ParkingSpot, Ticket, Abonne, Subscription
- **Entrée parking** : Attribution automatique d'une place selon dimensions
- **Sortie parking** : Calcul du prix (2€/heure) et libération de la place
- **Abonnements** : 2 types (Standard 50€/mois, Pack Garanti 100€/mois)
- **Statistiques** : Nombre de clients, revenus, taux d'occupation
- **Persistance** : Base SQLite avec Django ORM
- **Interface** : Vues HTML basiques

### ⚠️ Non implémentées (trop complexe/temps insuffisant)
- Téléporteurs (concept théorique du sujet)
- Service de livraison à domicile
- Service d'entretien/maintenance
- Système de réservation dans autres parkings

## Structure du projet

```
parking_app/
    models/         # Classes métier
        vehicle.py
        parking_spot.py
        ticket.py
        abonne.py
        subscription.py
    views/          # Contrôleurs
        enter_parking.py
        exit_parking.py
        statistics.py
    services/       # Logique métier
        parking_manager.py
    templates/      # Vues HTML
    tests/          # Tests unitaires
```

## Architecture
- **Pattern MVC** : Séparation modèles / vues / templates
- **Django** : Framework web Python
- **SQLite** : Base de données légère

## Utilisation

### Faire entrer une voiture
1. Aller sur `/enter/`
2. Remplir immatriculation, longueur, hauteur
3. (Optionnel) Cocher "Abonné" et remplir les infos
4. Soumettre → Une place est attribuée automatiquement

### Faire sortir une voiture
1. Aller sur `/exit/`
2. Entrer l'immatriculation
3. Le prix est calculé et affiché
4. La place est libérée

### Voir les statistiques
- Aller sur `/statistics/`
- Affichage du nombre de clients, revenus, etc.

## Tests
Lancer les tests :
```bash
python manage.py test parking_app
```

## Auteur
Oumar - L3 MIASHS Toulouse 2
Décembre 2025

## Notes
- Projet réalisé pour l'UE Python
- Certaines fonctionnalités du sujet (téléporteurs, livraison) ne sont pas implémentées car trop complexes
- Focus sur les fonctionnalités principales : entrée, sortie, abonnements, statistiques
