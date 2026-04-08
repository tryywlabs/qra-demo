from django.db import models


class GasDispersionCalculation(models.Model):
    class CalculationType(models.TextChoices):
        PLUME = "plume", "Gas plume dispersion"
        PUFF = "puff", "Gas puff dispersion"

    calculation_type = models.CharField(max_length=20, choices=CalculationType.choices)
    inputs = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def summary_value(self):
        return self.result.get("concentration")

    @property
    def result_preview(self):
        return {key: value for key, value in self.result.items() if key != "profile"}

    def __str__(self):
        value = self.summary_value
        summary = "no summary" if value is None else f"{value:.4f} {self.unit}"
        return f"{self.get_calculation_type_display()} = {summary}"
