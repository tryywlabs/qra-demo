from django.contrib import admin

from .models import FireCalculation


@admin.register(FireCalculation)
class FireCalculationAdmin(admin.ModelAdmin):
    list_display = ("calculation_type", "summary_value", "unit", "created_at")
    list_filter = ("calculation_type", "created_at")
    search_fields = ("calculation_type",)
