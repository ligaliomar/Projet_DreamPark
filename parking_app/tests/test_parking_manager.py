from django.test import TestCase
from datetime import datetime, timedelta
from parking_app.models import ParkingSpot, Vehicle, Ticket, Subscription, Abonne
from parking_app.services.parking_manager import ParkingManager


class ParkingManagerTest(TestCase):
    """Tests unitaires pour le service ParkingManager."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.manager = ParkingManager()
        
        # Créer plusieurs places de parking
        self.spot1 = ParkingSpot.objects.create(
            numero_place="A1",
            niveau=1,
            longueur_max=5.0,
            hauteur_max=2.5,
            est_occupee=False
        )
        self.spot2 = ParkingSpot.objects.create(
            numero_place="A2",
            niveau=1,
            longueur_max=6.0,
            hauteur_max=3.0,
            est_occupee=False
        )
        self.spot3 = ParkingSpot.objects.create(
            numero_place="B1",
            niveau=2,
            longueur_max=4.0,
            hauteur_max=2.0,
            est_occupee=False
        )

    def test_assign_place_success(self):
        """Test d'assignation réussie d'une place."""
        vehicle = Vehicle.objects.create(
            plaque_immat="ABC123",
            longueur=4.5,
            hauteur=2.0
        )
        spot = self.manager.attribuer_place(vehicle)
        
        self.assertIsNotNone(spot)
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.place_assignee, spot)
        
        spot.refresh_from_db()
        self.assertTrue(spot.est_occupee)

    def test_assign_place_creates_ticket(self):
        """Test que l'assignation crée un ticket."""
        vehicle = Vehicle.objects.create(
            plaque_immat="DEF456",
            longueur=4.0,
            hauteur=2.0
        )
        initial_count = Ticket.objects.count()
        self.manager.attribuer_place(vehicle)
        
        self.assertEqual(Ticket.objects.count(), initial_count + 1)
        ticket = Ticket.objects.get(vehicule=vehicle)
        self.assertEqual(ticket.vehicule, vehicle)

    def test_assign_place_compatible_dimensions(self):
        """Test que seules les places compatibles sont assignées."""
        # Véhicule trop grand pour spot3 (max 4.0 × 2.0)
        large_vehicle = Vehicle.objects.create(
            plaque_immat="GHI789",
            longueur=5.5,
            hauteur=2.8
        )
        spot = self.manager.attribuer_place(large_vehicle)
        
        # Doit choisir spot1 ou spot2, pas spot3
        self.assertIsNotNone(spot)
        self.assertIn(spot, [self.spot1, self.spot2])
        self.assertNotEqual(spot, self.spot3)

    def test_assign_place_with_subscription(self):
        """Test d'assignation avec abonnement."""
        abonne = Abonne.objects.create(
            nom="Test Abonné",
            email="test@example.com"
        )
        date_fin = datetime.now() + timedelta(days=365)
        subscription = Subscription.objects.create(
            abonne=abonne,
            type_formule="STANDARD",
            prix_mensuel=50.0,
            date_fin=date_fin
        )
        
        vehicle = Vehicle.objects.create(
            plaque_immat="JKL012",
            longueur=4.0,
            hauteur=2.0,
            type_abonnement=Vehicle.SubscriptionType.STANDARD
        )
        
        spot = self.manager.attribuer_place(vehicle, abonnement=subscription)
        
        self.assertIsNotNone(spot)
        ticket = Ticket.objects.get(vehicule=vehicle)
        self.assertEqual(ticket.abonnement, subscription)
        self.assertTrue(ticket.a_un_abonnement)

    def test_assign_place_parking_full(self):
        """Test quand le parking est plein."""
        # Occuper toutes les places
        self.spot1.est_occupee = True
        self.spot1.save()
        self.spot2.est_occupee = True
        self.spot2.save()
        self.spot3.est_occupee = True
        self.spot3.save()
        
        vehicle = Vehicle.objects.create(
            plaque_immat="MNO345",
            longueur=4.0,
            hauteur=2.0
        )
        
        spot = self.manager.attribuer_place(vehicle)
        self.assertIsNone(spot)

    def test_assign_place_no_compatible_spot(self):
        """Test quand aucune place n'est compatible."""
        # Véhicule trop grand pour toutes les places
        huge_vehicle = Vehicle.objects.create(
            plaque_immat="PQR678",
            longueur=10.0,
            hauteur=5.0
        )
        
        spot = self.manager.attribuer_place(huge_vehicle)
        self.assertIsNone(spot)

    def test_free_place(self):
        """Test de libération d'une place."""
        vehicle = Vehicle.objects.create(
            plaque_immat="STU901",
            longueur=4.0,
            hauteur=2.0
        )
        spot = self.manager.attribuer_place(vehicle)
        
        # Libérer la place
        self.manager.liberer_place(spot)
        
        spot.refresh_from_db()
        self.assertFalse(spot.est_occupee)
        
        vehicle.refresh_from_db()
        self.assertIsNone(vehicle.place_assignee)

    def test_update_display(self):
        """Test de la mise à jour du panneau (affichage console)."""
        # Cette méthode affiche dans la console, on teste juste qu'elle s'exécute
        self.manager.mettre_a_jour_panneau()
        # Pas d'assertion, juste vérifier qu'il n'y a pas d'erreur

    def test_multiple_assignments(self):
        """Test d'assignations multiples."""
        vehicles = []
        for i in range(3):
            vehicle = Vehicle.objects.create(
                plaque_immat=f"VEH{i}",
                longueur=4.0,
                hauteur=2.0
            )
            vehicles.append(vehicle)
        
        # Assigner les 3 véhicules
        spots = []
        for vehicle in vehicles:
            spot = self.manager.attribuer_place(vehicle)
            spots.append(spot)
        
        # Toutes les assignations doivent réussir
        for spot in spots:
            self.assertIsNotNone(spot)
        
        # Toutes les places doivent être occupées
        self.assertEqual(ParkingSpot.objects.filter(est_occupee=True).count(), 3)
