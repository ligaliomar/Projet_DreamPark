# Choix techniques et justifications

## Pourquoi Django ?
J'ai choisi Django parce que :
- On l'a vu en cours
- Ça permet de faire rapidement une interface web
- L'ORM simplifie la gestion de la base de données
- Le pattern MVT (Model-View-Template) correspond bien au sujet

## Architecture des modèles

### Vehicle (Véhicule)
- `plaque_immat` : identifiant unique de la voiture
- `longueur`, `hauteur` : pour vérifier si elle rentre dans la place
- `type_abonnement` : NONE, STANDARD ou GUARANTEED
- `place_assignee` : relation OneToOne vers ParkingSpot

**Choix :** OneToOneField car une voiture = une place max

### ParkingSpot (Place de parking)
- `numero_place` : identifiant unique (A12, B05...)
- `niveau` : étage du parking
- `longueur_max`, `hauteur_max` : dimensions acceptées
- `est_occupee` : booléen pour savoir si libre

**Choix :** Boolean pour `est_occupee` car plus simple que de vérifier si un véhicule y est

### Ticket
- Relation vers Vehicle (OneToOne)
- Relation vers Subscription (ForeignKey nullable)
- `heure_sortie`, `montant_paye` : pour la facturation

**Choix :** ForeignKey vers Subscription car un abonnement peut avoir plusieurs tickets

### Abonne et Subscription
Séparation en 2 classes :
- `Abonne` : les infos du client (nom, email...)
- `Subscription` : le contrat (type, prix, dates)

**Pourquoi séparé ?** Un abonné peut avoir plusieurs contrats successifs

## Algorithme d'attribution de place

```python
def attribuer_place(voiture):
    # 1. Filtre les places libres ET compatibles
    places = ParkingSpot.objects.filter(
        est_occupee=False,
        longueur_max >= voiture.longueur,
        hauteur_max >= voiture.hauteur
    )
    
    # 2. Prend la première dispo
    return places.first()
```

**Pourquoi `.first()` ?**
- Simple et fonctionnel
- On pourrait améliorer avec un tri (ex: place la plus proche de l'entrée)
- Mais le sujet demande pas d'optimisation particulière

## Calcul du prix

Tarif : 2€ / heure commencée

```python
duree = sortie - entree  # en secondes
heures = duree / 3600
heures_a_payer = int(heures) + (1 if heures % 1 > 0 else 0)
prix = heures_a_payer * 2
```

**Problème rencontré :**
- Au début j'utilisais `round()` mais ça arrondissait 1.4h à 1h
- Le sujet dit "heure commencée" donc il faut arrondir vers le HAUT
- Solution : `int() + 1` si il reste des minutes

## Gestion des abonnements

Deux types :
- STANDARD : 50€/mois, services de base
- GUARANTEED : 100€/mois, pack garanti (place réservée)

**Dans le code :**
- `Vehicle.type_abonnement` : enum pour le type
- `Ticket.abonnement` : ForeignKey optionnelle vers Subscription
- Si `abonnement` est None → client occasionnel

## Base de données

SQLite par défaut avec Django.

**Migrations :**
- `makemigrations` : crée les fichiers de migration
- `migrate` : applique les changements en BDD

**Problème :** Quand on change les noms de champs, il faut refaire une migration

## Interface web

3 vues principales :
1. **enter_parking** : formulaire d'entrée
2. **exit_parking** : formulaire de sortie
3. **statistics** : affichage des stats

**HTML basique** : pas de CSS complexe, juste du HTML simple
Le sujet demande une interface graphique, j'ai fait le minimum fonctionnel.

## Tests

Tests unitaires pour chaque classe :
- `test_vehicle.py`
- `test_parking_spot.py`
- `test_ticket.py`
- etc.

Format :
```python
def test_creation_vehicule(self):
    v = Vehicle.objects.create(...)
    self.assertEqual(v.plaque_immat, "AA-123-BB")
```

## Ce que je n'ai pas fait

### Téléporteurs
Le sujet parle de "téléporteurs" pour amener la voiture à sa place.
→ J'ai considéré que c'est juste conceptuel, pas à implémenter réellement

### Service de livraison
Le sujet mentionne qu'on peut faire livrer sa voiture à une adresse.
→ Trop complexe, nécessiterait un système de rendez-vous, d'adresses, etc.

### Pack garanti avec autres parkings
"Si le parking est plein, garer dans un autre parking"
→ Nécessiterait une BDD de parkings partenaires, pas fait

## Améliorations possibles

Si j'avais plus de temps :
- Meilleure interface CSS
- Système de réservation en ligne
- API REST pour mobile
- Optimisation de l'algorithme d'attribution (place la plus proche)
- Historique complet des passages
- Export PDF des tickets
- Gestion de plusieurs parkings
