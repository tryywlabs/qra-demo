from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import GasLeakForm, LiquidLeakForm, TwoPhaseLeakForm
from .models import LeakCalculation
from .services import (
    calculate_gas_leak,
    calculate_liquid_leak,
    calculate_two_phase_leak,
)

PANEL_CONFIG = {
    "gas": {
        "title": "Gas leak",
        "help_text": "Estimates gas mass release rate through a hole using diameter, gas density, and upstream gauge pressure.",
        "formula": "QG = 1.4 × 10^-4 × d^2 × sqrt(rho_g × P_g)",
        "form_class": GasLeakForm,
        "calculator": calculate_gas_leak,
        "record_type": LeakCalculation.CalculationType.GAS,
        "result_label": "QG",
    },
    "liquid": {
        "title": "Liquid leak",
        "help_text": "Estimates liquid mass release rate from a pressurized liquid leak using hole size, density, and pressure.",
        "formula": "QL = 2.1 × 10^-4 × d^2 × sqrt(rho_L × P_L)",
        "form_class": LiquidLeakForm,
        "calculator": calculate_liquid_leak,
        "record_type": LeakCalculation.CalculationType.LIQUID,
        "result_label": "QL",
    },
    "two_phase": {
        "title": "Two-phase leak",
        "help_text": "Blends gas and liquid release contributions into one equivalent two-phase release rate using the gas-oil ratio.",
        "formula": "QO = (GOR / (GOR + 1)) × QG + (1 / (GOR + 1)) × QL",
        "form_class": TwoPhaseLeakForm,
        "calculator": calculate_two_phase_leak,
        "record_type": LeakCalculation.CalculationType.TWO_PHASE,
        "result_label": "QO",
    },
}


def _build_forms(post_data=None, submitted_panel=None):
    forms = {}
    for panel_key, config in PANEL_CONFIG.items():
        form_class = config["form_class"]
        if post_data is not None and panel_key == submitted_panel:
            forms[panel_key] = form_class(post_data, prefix=panel_key)
        else:
            forms[panel_key] = form_class(prefix=panel_key)
    return forms


def dashboard(request):
    selected_panel = "gas"
    forms = _build_forms()
    panel_results = {}

    if request.method == "POST":
        selected_panel = request.POST.get("calculator", selected_panel)
        forms = _build_forms(request.POST, selected_panel)

        if selected_panel in PANEL_CONFIG:
            form = forms[selected_panel]
            panel = PANEL_CONFIG[selected_panel]
            if form.is_valid():
                inputs = {
                    key: float(value)
                    for key, value in form.cleaned_data.items()
                }
                result = panel["calculator"](**inputs)
                record = LeakCalculation.objects.create(
                    calculation_type=panel["record_type"],
                    inputs=inputs,
                    result=result,
                )
                panel_results[selected_panel] = {
                    "label": panel["result_label"],
                    "value": result,
                    "unit": record.unit,
                }

    recent_calculations = LeakCalculation.objects.all()[:8]
    panel_cards = []
    for panel_key, panel in PANEL_CONFIG.items():
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
        "panel_cards": panel_cards,
        "recent_calculations": recent_calculations,
        "selected_panel": selected_panel,
    }
    return render(request, "dashboard.html", context)


@require_POST
def clear_history(request):
    LeakCalculation.objects.all().delete()
    return redirect("leak:dashboard")
