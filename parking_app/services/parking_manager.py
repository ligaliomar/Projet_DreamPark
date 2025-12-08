from datetime import datetime
from typing import Optional

from parking_app.models.parking_spot import ParkingSpot
from parking_app.models.vehicle import Vehicle
from parking_app.models.ticket import Ticket


class ParkingManager:
    """
    Gère l'assignation et la libération des places dans DreamPark.
    """

    def assign_place(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Tente d'assigner une place au véhicule.
        Retourne la place assignée ou None si aucune place n'est adaptée.
        """

        # Récupération des places libres compatibles
        spots = ParkingSpot.objects.filter(
            is_occupied=False,
            max_length__gte=vehicle.length,
            max_height__gte=vehicle.height
        )

        if not spots.exists():
            return None  # Parking plein

        # On prend la première place libre adaptée
        spot = spots.first()

        # 1) Assigner la place au véhicule
        vehicle.assigned_spot = spot
        vehicle.save()

        # 2) Marquer la place comme occupée
        spot.is_occupied = True
        spot.save()

        # 3) Créer un ticket
        Ticket.objects.create(
            vehicle=vehicle,
            is_subscription=False,
            payment_method="cash"
        )

        # 4) Mise à jour du panneau (console pour l'instant)
        self.update_display()

        return spot

    def free_place(self, spot: ParkingSpot):
        """
        Libère une place de parking.
        """

        # 1) Libérer la place
        spot.is_occupied = False
        spot.save()

        # 2) Retirer la place du véhicule (si un véhicule y était)
        Vehicle.objects.filter(assigned_spot=spot).update(assigned_spot=None)

        # 3) Mise à jour de l'affichage
        self.update_display()

    def update_display(self):
        """
        Affiche dans la console le nombre de places disponibles.
        """
        free = ParkingSpot.objects.filter(is_occupied=False).count()
        print(f"[PANNEAU] Places disponibles : {free}")