from django.test import TestCase
from parking_app.models import ParkingSpot, Vehicle
from parking_app.services.parking_manager import ParkingManager

# parking_app/tests/test_parking_manager_spec.py
from django.test import TestCase
from parking_app.models.parking_spot import ParkingSpot
from parking_app.models.vehicle import Vehicle

class ParkingManagerTestCase(TestCase):
    def setUp(self):
        # Création de places de parking
        self.spot1 = ParkingSpot.objects.create(
            identifier="A1",
            level=1,
            max_length=5.0,
            max_height=2.0,
            is_occupied=False
        )
        self.spot2 = ParkingSpot.objects.create(
            identifier="B1",
            level=1,
            max_length=4.0,
            max_height=1.8,
            is_occupied=False
        )

        # Création d'un véhicule
        self.vehicle = Vehicle.objects.create(
            plate_number="ABC-123",
            length=4.5,
            height=1.8
        )

    def test_assign_place_success(self):
        """
        Vérifie qu'un véhicule peut être assigné à une place adaptée.
        """
        # Logique simple d'assignation (exemple)
        available_spots = ParkingSpot.objects.filter(
            max_length__gte=self.vehicle.length,
            max_height__gte=self.vehicle.height,
            is_occupied=False
        )

        self.assertTrue(available_spots.exists(), "Aucune place disponible adaptée au véhicule")

        spot_to_assign = available_spots.first()
        self.vehicle.assigned_spot = spot_to_assign
        self.vehicle.save()

        # Marquer la place comme occupée
        spot_to_assign.is_occupied = True
        spot_to_assign.save()

        # Vérifications
        self.vehicle.refresh_from_db()
        spot_to_assign.refresh_from_db()
        self.assertEqual(self.vehicle.assigned_spot, spot_to_assign)
        self.assertTrue(spot_to_assign.is_occupied)