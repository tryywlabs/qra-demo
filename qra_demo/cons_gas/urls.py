from django.urls import path

from .views import clear_gas_dispersion_history, gas_dispersion_dashboard


urlpatterns = [
    path("gas-dispersion/", gas_dispersion_dashboard, name="gas_dispersion_dashboard"),
    path(
        "gas-dispersion/clear-history/",
        clear_gas_dispersion_history,
        name="clear_gas_dispersion_history",
    ),
]
