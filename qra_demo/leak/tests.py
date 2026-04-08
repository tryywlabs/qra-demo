from django.test import TestCase
from django.urls import reverse

from .models import LeakCalculation


class DashboardViewTests(TestCase):
    def test_home_page_renders_module_links(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consequence Demo")
        self.assertContains(response, reverse("leak:dashboard"))
        self.assertContains(response, reverse("gas_dispersion_dashboard"))

    def test_dashboard_renders(self):
        response = self.client.get(reverse("leak:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "QRA Leak Calculators")

    def test_gas_panel_submission_creates_record(self):
        response = self.client.post(
            reverse("leak:dashboard"),
            {
                "calculator": "gas",
                "gas-diameter_mm": 10,
                "gas-density_kg_m3": 1.2,
                "gas-pressure_bar_gauge": 40,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(LeakCalculation.objects.count(), 1)
        record = LeakCalculation.objects.get()
        self.assertEqual(record.calculation_type, LeakCalculation.CalculationType.GAS)
        self.assertContains(response, "Qg")
    
    def test_clear_history(self):
        LeakCalculation.objects.create(
            calculation_type=LeakCalculation.CalculationType.GAS,
            inputs={"diameter_mm": 10, "density_kg_m3": 1.2, "pressure_bar_gauge": 40},
            result=0.001,
        )
        response = self.client.post(reverse("leak:clear_history"))

        self.assertRedirects(response, reverse("leak:dashboard"))
        self.assertEqual(LeakCalculation.objects.count(), 0)

    def test_fire_directory_page_renders(self):
        response = self.client.get(reverse("fire_directory"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pool_fire.py")
