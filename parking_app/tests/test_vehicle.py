from django.test import TestCase
from parking_app.models import Vehicle, ParkingSpot


class VehicleModelTest(TestCase):
    """Tests unitaires pour le modèle Vehicle."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.spot = ParkingSpot.objects.create(
            numero_place="A1",
            niveau=1,
            longueur_max=5.0,
            hauteur_max=2.5
        )

    def test_create_vehicle_occasionnel(self):
        """Test de création d'un véhicule occasionnel."""
        vehicle = Vehicle.objects.create(
            plaque_immat="ABC123",
            longueur=4.5,
            hauteur=1.8,
            type_abonnement=Vehicle.SubscriptionType.NONE
        )
        self.assertEqual(vehicle.plaque_immat, "ABC123")
        self.assertEqual(vehicle.longueur, 4.5)
        self.assertEqual(vehicle.hauteur, 1.8)
        self.assertEqual(vehicle.type_abonnement, Vehicle.SubscriptionType.NONE)
        self.assertIsNone(vehicle.place_assignee)

    def test_create_vehicle_abonne(self):
        """Test de création d'un véhicule abonné."""
        vehicle = Vehicle.objects.create(
            plaque_immat="DEF456",
            longueur=4.0,
            hauteur=2.0,
            type_abonnement=Vehicle.SubscriptionType.STANDARD
        )
        self.assertEqual(vehicle.type_abonnement, Vehicle.SubscriptionType.STANDARD)

    def test_create_vehicle_pack_garanti(self):
        """Test de création d'un véhicule avec pack garanti."""
        vehicle = Vehicle.objects.create(
            plaque_immat="GHI789",
            longueur=5.5,
            hauteur=2.2,
            type_abonnement=Vehicle.SubscriptionType.GUARANTEED
        )
        self.assertEqual(vehicle.type_abonnement, Vehicle.SubscriptionType.GUARANTEED)

    def test_assign_spot_to_vehicle(self):
        """Test de l'assignation d'une place à un véhicule."""
        vehicle = Vehicle.objects.create(
            plaque_immat="JKL012",
            longueur=4.0,
            hauteur=2.0
        )
        vehicle.place_assignee = self.spot
        vehicle.save()
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.place_assignee, self.spot)

    def test_vehicle_str(self):
        """Test de la représentation string d'un véhicule."""
        vehicle = Vehicle.objects.create(
            plaque_immat="MNO345",
            longueur=4.0,
            hauteur=2.0
        )
        self.assertEqual(str(vehicle), "MNO345")

    def test_vehicle_entry_time_auto_set(self):
        """Test que entry_time est automatiquement défini."""
        vehicle = Vehicle.objects.create(
            plaque_immat="PQR678",
            longueur=4.0,
            hauteur=2.0
        )
        self.assertIsNotNone(vehicle.heure_entree)

    def test_default_subscription_type_is_none(self):
        """Test que le type par défaut est NONE."""
        vehicle = Vehicle.objects.create(
            plaque_immat="STU901",
            longueur=4.0,
            hauteur=2.0
        )
        self.assertEqual(vehicle.type_abonnement, Vehicle.SubscriptionType.NONE)
