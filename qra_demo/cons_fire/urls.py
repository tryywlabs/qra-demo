from django.urls import path

from .views import clear_fire_history, fire_dashboard


urlpatterns = [
    path("fire/", fire_dashboard, name="fire_dashboard"),
    path("fire/clear-history/", clear_fire_history, name="clear_fire_history"),
]
