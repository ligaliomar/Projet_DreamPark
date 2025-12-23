from datetime import datetime
from typing import Optional

from parking_app.models.parking_spot import ParkingSpot
from parking_app.models.vehicle import Vehicle
from parking_app.models.ticket import Ticket


class ParkingManager:
    """
    Classe qui gere l'assignation et la liberation des places
    C'est le composant principal du systeme de parking DreamPark
    """

    def attribuer_place(self, voiture: Vehicle, abonnement=None) -> Optional[ParkingSpot]:
        """
        Essaye de trouver une place pour la voiture
        Retourne la place si on en trouve une, sinon None (parking plein)
        """

        # Je cherche toutes les places qui sont libres et assez grandes
        places_possibles = ParkingSpot.objects.filter(
            est_occupee=False,
            longueur_max__gte=voiture.longueur,
            hauteur_max__gte=voiture.hauteur
        )

        # Si y'a aucune place dispo, on retourne None
        if not places_possibles.exists():
            return None  # parking complet

        # Je prends la premiere place qui convient
        place = places_possibles.first()

        # Etape 1: j'assigne la place a la voiture
        voiture.place_assignee = place
        voiture.save()

        # Etape 2: je marque la place comme occupee
        place.est_occupee = True
        place.save()

        # Etape 3: creation du ticket (comme dans le sujet)
        a_abonnement = abonnement is not None
        Ticket.objects.create(
            vehicule=voiture,
            abonnement=abonnement,
            a_un_abonnement=a_abonnement,
            mode_paiement="cash"  # par defaut especes
        )

        # Etape 4: mise a jour du panneau d'affichage
        self.mettre_a_jour_panneau()

        return place

    def liberer_place(self, place: ParkingSpot):
        """
        Libere une place quand une voiture sort du parking
        """

        # Je remets la place en mode disponible
        place.est_occupee = False
        place.save()

        # J'enleve la place assignee au vehicule qui etait la
        Vehicle.objects.filter(place_assignee=place).update(place_assignee=None)

        # Mise a jour du panneau
        self.mettre_a_jour_panneau()

    def mettre_a_jour_panneau(self):
        """
        Met a jour l'affichage du nombre de places dispo
        (comme dit dans le sujet avec les panneaux aux acces)
        """
        nb_places_libres = ParkingSpot.objects.filter(est_occupee=False).count()
        print(f"[PANNEAU AFFICHAGE] Places disponibles : {nb_places_libres}")