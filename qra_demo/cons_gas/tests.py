from django.test import TestCase
from django.urls import reverse

from .models import GasDispersionCalculation


class GasDispersionDashboardTests(TestCase):
    def test_dashboard_renders(self):
        response = self.client.get(reverse("gas_dispersion_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gas Dispersion Calculators")

    def test_plume_submission_creates_record(self):
        response = self.client.post(
            reverse("gas_dispersion_dashboard"),
            {
                "calculator": "plume",
                "plume-release_rate_kg_s": 1.2,
                "plume-wind_speed_m_s": 5.0,
                "plume-release_height_m": 2.0,
                "plume-downwind_distance_m": 100.0,
                "plume-crosswind_distance_m": 0.0,
                "plume-receptor_height_m": 1.5,
                "plume-stability_class": "D",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(GasDispersionCalculation.objects.count(), 1)
        record = GasDispersionCalculation.objects.get()
        self.assertEqual(record.calculation_type, GasDispersionCalculation.CalculationType.PLUME)
        self.assertIn("concentration", record.result)
        self.assertContains(response, "sigma_y")

    def test_clear_history(self):
        GasDispersionCalculation.objects.create(
            calculation_type=GasDispersionCalculation.CalculationType.PUFF,
            inputs={"released_mass_kg": 50},
            result={"concentration": 0.2, "sigma_y": 1.0, "sigma_z": 2.0},
            unit="kg/m^3",
        )

        response = self.client.post(reverse("clear_gas_dispersion_history"))

        self.assertRedirects(response, reverse("gas_dispersion_dashboard"))
        self.assertEqual(GasDispersionCalculation.objects.count(), 0)
