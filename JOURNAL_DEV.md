# Journal de développement - Projet Parking DreamPark

## 19 décembre 2025
**Début du projet**
- J'ai commencé par lire le sujet et comprendre ce qu'il fallait faire
- C'est un système de gestion de parking avec des places, des véhicules et des tickets
- Le truc des téléporteurs c'est un peu bizarre mais bon c'est de la SF

## 20 décembre 2025
**Mise en place des modèles**
- J'ai créé les classes principales : Vehicle, ParkingSpot, Ticket
- Au début j'avais oublié de mettre les dimensions (longueur/hauteur) sur les places
- J'ai dû corriger ça sinon ça marchait pas pour vérifier si la voiture rentre

**Problèmes rencontrés :**
- Erreur "ForeignKey requires on_delete" → j'avais oublié le on_delete=models.CASCADE
- Confus entre OneToOneField et ForeignKey au début

## 21 décembre 2025
**Développement du système d'abonnement**
- Ajout de la classe Abonne et Subscription
- J'ai fait 2 types : STANDARD et GUARANTEED (pack garanti)
- Prix : 50€/mois pour standard, 100€/mois pour pack garanti

**Bug résolu :**
- Les abonnés avaient pas de lien avec les tickets au début
- J'ai ajouté un ForeignKey dans Ticket vers Subscription

## 22 décembre 2025  
**Interface web (vues Django)**
- Création de enter_parking_view pour faire entrer les voitures
- Création de exit_parking pour la sortie et le paiement
- Au début le calcul de prix marchait pas, j'avais oublié d'arrondir à l'heure supérieure

**Problème de calcul :**
- Premier essai : hours * 2 → problème si 1.5h on payait 3€
- Correction : il faut arrondir vers le haut, donc int(hours) + 1 si reste

## 23 décembre 2025
**Tests et statistiques**
- Ajout de la vue statistics pour voir le nombre de clients, revenus etc
- Les tests unitaires c'est long à écrire mais ça permet de vérifier que tout fonctionne
- J'ai testé manuellement aussi en créant des voitures

**À faire :**
- Peut-être ajouter plus de statistiques
- Améliorer l'interface HTML (c'est un peu basique pour l'instant)
- Tester avec plus de cas limites

## Difficultés principales
1. Comprendre les relations entre les tables (ForeignKey vs OneToOne)
2. Le système d'abonnement était pas clair au début
3. Les migrations Django des fois ça plante, faut faire makemigrations puis migrate
4. J'ai passé du temps sur le calcul de prix, fallait bien gérer les heures

## Points positifs
- Le pattern MVC c'est pratique, ça sépare bien le code
- Django ORM facilite les requêtes en base
- Les tests aident à vérifier que ça marche

## Notes perso
- Le sujet parle de téléporteurs mais bon j'ai pas implémenté ça en vrai
- Le service de livraison aussi c'est mentionné mais c'est trop complexe pour le temps donné
- J'ai surtout focalisé sur les fonctionnalités principales
