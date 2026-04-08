from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import PoolFireForm
from .models import FireCalculation
from .services import calculate_pool_fire_model


FIRE_PANEL_CONFIG = {
    "pool_fire": {
        "title": "Pool fire",
        "help_text": (
            "Thermal radiation model for a steady pool fire.\n"
            "\n"
            "Calculates flame geometry, soot effects, emissive power, and the resulting heat flux at a specified separation distance."
        ),
        "formula": "Qrad = E_bar x Fv x tau_atm",
        "form_class": PoolFireForm,
        "calculator": calculate_pool_fire_model,
        "record_type": FireCalculation.CalculationType.POOL_FIRE,
        "result_label": "Qrad",
        "unit": "kW/m^2",
        "primary_key": "radiation_flux",
        "details": (
            ("flame_length", "Flame length"),
            ("mean_emissive_power", "Mean emissive power"),
            ("view_factor", "View factor"),
            ("tau_atm", "Atmospheric transmissivity"),
        ),
    },
}


def _build_forms(post_data=None, submitted_panel=None):
    forms = {}
    for panel_key, config in FIRE_PANEL_CONFIG.items():
        form_class = config["form_class"]
        if post_data is not None and panel_key == submitted_panel:
            forms[panel_key] = form_class(post_data, prefix=panel_key)
        else:
            forms[panel_key] = form_class(prefix=panel_key)
    return forms


def _result_details(result, panel):
    details = []
    for key, label in panel["details"]:
        value = result.get(key)
        if value is not None:
            details.append({"label": label, "value": value})
    return details


def fire_dashboard(request):
    selected_panel = "pool_fire"
    forms = _build_forms()
    panel_results = {}

    if request.method == "POST":
        selected_panel = request.POST.get("calculator", selected_panel)
        forms = _build_forms(request.POST, selected_panel)

        if selected_panel in FIRE_PANEL_CONFIG:
            form = forms[selected_panel]
            panel = FIRE_PANEL_CONFIG[selected_panel]
            if form.is_valid():
                inputs = dict(form.cleaned_data)
                result = panel["calculator"](**inputs)
                FireCalculation.objects.create(
                    calculation_type=panel["record_type"],
                    inputs=inputs,
                    result=result,
                    unit=panel["unit"],
                )
                panel_results[selected_panel] = {
                    "label": panel["result_label"],
                    "value": result[panel["primary_key"]],
                    "unit": panel["unit"],
                    "details": _result_details(result, panel),
                }

    recent_calculations = FireCalculation.objects.all()[:8]
    panel_cards = []
    for panel_key, panel in FIRE_PANEL_CONFIG.items():
        panel_cards.append(
            {
                "key": panel_key,
                "title": panel["title"],
                "help_text": panel["help_text"],
                "formula": panel["formula"],
                "result_label": panel["result_label"],
                "form": forms[panel_key],
                "result": panel_results.get(panel_key),
            }
        )

    context = {
        "workspace": {
            "eyebrow": "Consequence Demo / Fire",
            "title": "Fire Calculators",
            "description": "Run the modular pool-fire model and estimate thermal radiation at a specified separation distance.",
            "history_copy": "Saved pool-fire radiation runs from the fire workspace.",
            "accent": "#bd5b24",
            "accent_deep": "#8f4218",
            "accent_soft": "rgba(189, 91, 36, 0.14)",
            "empty_copy": "No fire calculations saved yet.",
        },
        "panel_cards": panel_cards,
        "recent_calculations": recent_calculations,
        "selected_panel": selected_panel,
        "clear_url_name": "clear_fire_history",
    }
    return render(request, "consequence/dashboard.html", context)


@require_POST
def clear_fire_history(request):
    FireCalculation.objects.all().delete()
    return redirect("fire_dashboard")
