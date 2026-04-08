from django.test import TestCase
from django.urls import reverse

from .models import ExplosionCalculation


class ExplosionDashboardTests(TestCase):
    def test_dashboard_renders(self):
        response = self.client.get(reverse("explosion_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explosion Calculators")

    def test_tnt_submission_creates_record(self):
        response = self.client.post(
            reverse("explosion_dashboard"),
            {
                "calculator": "tnt",
                "tnt-efficiency": 0.06,
                "tnt-mass_kg": 120.0,
                "tnt-heat_combustion_kj_kg": 50000.0,
                "tnt-tnt_heat_combustion_kj_kg": 4680.0,
                "tnt-distance_m": 25.0,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExplosionCalculation.objects.count(), 1)
        record = ExplosionCalculation.objects.get()
        self.assertEqual(record.calculation_type, ExplosionCalculation.CalculationType.TNT)
        self.assertIn("peak_overpressure", record.result)
        self.assertContains(response, "TNT mass")

    def test_clear_history(self):
        ExplosionCalculation.objects.create(
            calculation_type=ExplosionCalculation.CalculationType.BST,
            inputs={"energy_kj": 750000},
            result={"energy_kj": 750000, "scaled_distance": 1.4, "peak_overpressure": 0.5},
            unit="bar",
        )

        response = self.client.post(reverse("clear_explosion_history"))

        self.assertRedirects(response, reverse("explosion_dashboard"))
        self.assertEqual(ExplosionCalculation.objects.count(), 0)
