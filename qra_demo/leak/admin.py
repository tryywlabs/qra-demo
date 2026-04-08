from django.contrib import admin

from .models import LeakCalculation


@admin.register(LeakCalculation)
class LeakCalculationAdmin(admin.ModelAdmin):
    list_display = ("calculation_type", "result", "unit", "created_at")
    list_filter = ("calculation_type", "created_at")
    search_fields = ("calculation_type",)
