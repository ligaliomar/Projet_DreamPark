from django.test import TestCase
from parking_app.models import Abonne


class AbonneModelTest(TestCase):
    """Tests unitaires pour le modèle Abonne."""

    def test_create_abonne(self):
        """Test de création d'un abonné."""
        abonne = Abonne.objects.create(
            nom="Jean Dupont",
            email="jean.dupont@example.com",
            telephone="0612345678"
        )
        self.assertEqual(abonne.nom, "Jean Dupont")
        self.assertEqual(abonne.email, "jean.dupont@example.com")
        self.assertEqual(abonne.telephone, "0612345678")
        self.assertTrue(abonne.is_active)
        self.assertIsNotNone(abonne.created_at)

    def test_abonne_str(self):
        """Test de la représentation string d'un abonné."""
        abonne = Abonne.objects.create(
            nom="Marie Martin",
            email="marie.martin@example.com"
        )
        self.assertEqual(str(abonne), "Marie Martin (actif)")

    def test_abonne_str_inactive(self):
        """Test de la représentation string d'un abonné inactif."""
        abonne = Abonne.objects.create(
            nom="Pierre Durand",
            email="pierre.durand@example.com",
            is_active=False
        )
        self.assertEqual(str(abonne), "Pierre Durand (inactif)")

    def test_email_unique(self):
        """Test que l'email est unique."""
        Abonne.objects.create(
            nom="Test User 1",
            email="test@example.com"
        )
        with self.assertRaises(Exception):
            Abonne.objects.create(
                nom="Test User 2",
                email="test@example.com"  # Même email
            )

    def test_telephone_optional(self):
        """Test que le téléphone est optionnel."""
        abonne = Abonne.objects.create(
            nom="Sans Téléphone",
            email="sans.tel@example.com",
            telephone=""
        )
        self.assertEqual(abonne.telephone, "")

    def test_default_is_active_true(self):
        """Test que is_active est True par défaut."""
        abonne = Abonne.objects.create(
            nom="Actif Par Défaut",
            email="actif@example.com"
        )
        self.assertTrue(abonne.is_active)

    def test_deactivate_abonne(self):
        """Test de la désactivation d'un abonné."""
        abonne = Abonne.objects.create(
            nom="À Désactiver",
            email="desactiver@example.com"
        )
        abonne.is_active = False
        abonne.save()
        abonne.refresh_from_db()
        self.assertFalse(abonne.is_active)
