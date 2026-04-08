from django.db import models


class LeakCalculation(models.Model):
    class CalculationType(models.TextChoices):
        GAS = "gas", "Gas leak"
        LIQUID = "liquid", "Liquid leak"
        TWO_PHASE = "two_phase", "Two-phase leak"

    calculation_type = models.CharField(max_length=20, choices=CalculationType.choices)
    inputs = models.JSONField(default=dict)
    result = models.FloatField()
    unit = models.CharField(max_length=20, default="kg/s")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_calculation_type_display()} = {self.result:.4f} {self.unit}"
