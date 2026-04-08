from django.urls import path

from .views import dashboard, clear_history


app_name = "leak"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("clear-history/", clear_history, name="clear_history"),
]
