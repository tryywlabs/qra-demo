from django.db import models


class FireCalculation(models.Model):
    class CalculationType(models.TextChoices):
        POOL_FIRE = "pool_fire", "Pool fire"

    calculation_type = models.CharField(max_length=20, choices=CalculationType.choices)
    inputs = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def summary_value(self):
        return self.result.get("radiation_flux")

    @property
    def result_preview(self):
        return self.result

    def __str__(self):
        value = self.summary_value
        summary = "no summary" if value is None else f"{value:.4f} {self.unit}"
        return f"{self.get_calculation_type_display()} = {summary}"
