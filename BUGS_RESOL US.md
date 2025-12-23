# Bugs rencontrés et résolus

## Bug #1 : ForeignKey sans on_delete
**Date :** 20 décembre

**Erreur :**
```
TypeError: __init__() missing 1 required positional argument: 'on_delete'
```

**Cause :** J'avais écrit `ForeignKey(Abonne)` au lieu de `ForeignKey(Abonne, on_delete=...)`

**Solution :** Ajout de `on_delete=models.CASCADE` sur tous les ForeignKey

---

## Bug #2 : Calcul de prix incorrect
**Date :** 22 décembre

**Problème :** 
- Voiture garée 1h30 → payait 3€ au lieu de 4€
- Le `round()` arrondissait mal

**Code bugué :**
```python
hours = duration.total_seconds() / 3600
return round(hours) * 2  # ❌ round(1.5) = 2, donc 4€ OK
                         # ❌ round(1.4) = 1, donc 2€ FAUX
```

**Solution :**
```python
heures_a_payer = int(nb_heures)
if nb_heures % 1 > 0:
    heures_a_payer += 1
```

---

## Bug #3 : Migration échouée
**Date :** 21 décembre

**Erreur :**
```
django.db.utils.OperationalError: no such table: parking_app_vehicle
```

**Cause :** J'avais oublié de faire `python manage.py migrate` après `makemigrations`

**Solution :** Toujours faire les 2 commandes :
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Bug #4 : Voiture déjà dans le parking
**Date :** 22 décembre

**Problème :** On pouvait faire entrer 2 fois la même plaque

**Code manquant :**
```python
if Vehicle.objects.filter(plaque_immat=plaque, place_assignee__isnull=False).exists():
    return HttpResponse("❌ Déjà garé")
```

**Solution :** Vérification avant de créer le véhicule

---

## Bug #5 : Place pas libérée à la sortie
**Date :** 22 décembre

**Problème :** Quand une voiture sortait, la place restait marquée comme occupée

**Cause :** J'avais oublié de mettre à jour `est_occupee`

**Correction :**
```python
place.est_occupee = False
place.save()
```

---

## Bug #6 : Import circulaire
**Date :** 20 décembre

**Erreur :**
```
ImportError: cannot import name 'Vehicle' from partially initialized module
```

**Cause :** `vehicle.py` importait `Ticket` et `ticket.py` importait `Vehicle`

**Solution :** Réorganisation des imports, mettre les imports dans les méthodes si nécessaire

---

## Bug #7 : Abonnement mal créé
**Date :** 21 décembre

**Problème :** L'email de l'abonné devait être unique, mais j'essayais de créer 2 fois le même

**Code bugué :**
```python
abonne = Abonne.objects.create(email="test@test.com")  # OK
abonne2 = Abonne.objects.create(email="test@test.com")  # ❌ Erreur unique constraint
```

**Solution :** Vérifier si l'abonné existe déjà :
```python
abonne, created = Abonne.objects.get_or_create(
    email=email_abonne,
    defaults={'nom': nom_abonne}
)
```

---

## Bug #8 : Template introuvable
**Date :** 22 décembre

**Erreur :**
```
TemplateDoesNotExist: parking_app/enter_parking.html
```

**Cause :** Le fichier était dans `templates/` au lieu de `templates/parking_app/`

**Solution :** Respecter l'arborescence Django :
```
parking_app/
    templates/
        parking_app/    ← Sous-dossier avec le nom de l'app
            enter_parking.html
```

---

## Bug #9 : Statistiques vides
**Date :** 23 décembre

**Problème :** `total_revenus` affichait None au lieu de 0

**Code bugué :**
```python
total_revenus = Ticket.objects.aggregate(Sum('montant_paye'))['montant_paye__sum']
# Retourne None si aucun ticket
```

**Solution :**
```python
total_revenus = Ticket.objects.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
```

---

## Problèmes non résolus

### Performance avec beaucoup de places
Si le parking a 10000 places, le filtre `ParkingSpot.objects.filter(...)` pourrait être lent.

**Solution possible :** Ajouter des index sur `est_occupee`, `longueur_max`, `hauteur_max`

### Pas de gestion de concurrence
Si 2 voitures demandent la même place en même temps, y'a un risque.

**Solution possible :** Utiliser des transactions Django (`@transaction.atomic`)
