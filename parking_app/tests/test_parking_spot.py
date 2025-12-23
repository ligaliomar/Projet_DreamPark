from django.test import TestCase
from parking_app.models import ParkingSpot


class ParkingSpotModelTest(TestCase):
    """Tests unitaires pour le modèle ParkingSpot."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.spot = ParkingSpot.objects.create(
            numero_place="A1",
            niveau=1,
            longueur_max=5.0,
            hauteur_max=2.5,
            est_occupee=False
        )

    def test_create_parking_spot(self):
        """Test de création d'une place de parking."""
        self.assertEqual(self.spot.numero_place, "A1")
        self.assertEqual(self.spot.niveau, 1)
        self.assertEqual(self.spot.longueur_max, 5.0)
        self.assertEqual(self.spot.hauteur_max, 2.5)
        self.assertFalse(self.spot.est_occupee)

    def test_parking_spot_str(self):
        """Test de la représentation string d'une place."""
        expected = "A1 (Niveau 1)"
        self.assertEqual(str(self.spot), expected)

    def test_unique_identifier(self):
        """Test que l'identifiant est unique."""
        with self.assertRaises(Exception):
            ParkingSpot.objects.create(
                numero_place="A1",  # Même identifiant
                niveau=2,
                longueur_max=4.0,
                hauteur_max=2.0
            )

    def test_toggle_occupation(self):
        """Test de la modification du statut d'occupation."""
        self.assertFalse(self.spot.est_occupee)
        self.spot.est_occupee = True
        self.spot.save()
        self.spot.refresh_from_db()
        self.assertTrue(self.spot.est_occupee)

    def test_spot_dimensions(self):
        """Test que les dimensions sont correctement stockées."""
        spot = ParkingSpot.objects.create(
            numero_place="B2",
            niveau=2,
            longueur_max=6.5,
            hauteur_max=3.0
        )
        self.assertEqual(spot.longueur_max, 6.5)
        self.assertEqual(spot.hauteur_max, 3.0)
