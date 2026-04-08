from django.urls import path

from .views import clear_explosion_history, explosion_dashboard


urlpatterns = [
    path("explosion/", explosion_dashboard, name="explosion_dashboard"),
    path(
        "explosion/clear-history/",
        clear_explosion_history,
        name="clear_explosion_history",
    ),
]
