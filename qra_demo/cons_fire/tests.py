from django.test import TestCase
from django.urls import reverse

from .models import FireCalculation


class FireDashboardTests(TestCase):
    def test_dashboard_renders(self):
        response = self.client.get(reverse("fire_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fire Calculators")
        self.assertContains(response, "Pool fire")

    def test_pool_fire_submission_creates_record(self):
        response = self.client.post(
            reverse("fire_dashboard"),
            {
                "calculator": "pool_fire",
                "pool_fire-fuel": "LNG",
                "pool_fire-D": 30.0,
                "pool_fire-U": 5.0,
                "pool_fire-rho": 1.205,
                "pool_fire-g": 9.81,
                "pool_fire-A": 55.0,
                "pool_fire-p": 0.6666667,
                "pool_fire-q": -0.21,
                "pool_fire-r": 17.17,
                "pool_fire-beta": 0.06,
                "pool_fire-dHc": 50000.0,
                "pool_fire-Ca": 1.0,
                "pool_fire-Ta": 293.15,
                "pool_fire-Emax": 325.0,
                "pool_fire-Dopt": 13.8,
                "pool_fire-k_m": 130.0,
                "pool_fire-Lb_factor": 0.6,
                "pool_fire-S": 10.0,
                "pool_fire-H_override": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FireCalculation.objects.count(), 1)
        record = FireCalculation.objects.get()
        self.assertEqual(record.calculation_type, FireCalculation.CalculationType.POOL_FIRE)
        self.assertIn("radiation_flux", record.result)
        self.assertContains(response, "Mean emissive power")

    def test_clear_history(self):
        FireCalculation.objects.create(
            calculation_type=FireCalculation.CalculationType.POOL_FIRE,
            inputs={"fuel": "LNG", "D": 30.0},
            result={"radiation_flux": 68.6, "flame_length": 53.9},
            unit="kW/m^2",
        )

        response = self.client.post(reverse("clear_fire_history"))

        self.assertRedirects(response, reverse("fire_dashboard"))
        self.assertEqual(FireCalculation.objects.count(), 0)
