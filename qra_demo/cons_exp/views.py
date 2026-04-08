from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import BSTExplosionForm, TNOExplosionForm, TNTExplosionForm
from .models import ExplosionCalculation
from .services import (
    calculate_bst_overpressure,
    calculate_tno_overpressure,
    calculate_tnt_equivalency,
)

EXPLOSION_PANEL_CONFIG = {
    "tnt": {
        "title": "TNT equivalency",
        "help_text": (
            "Uses empirical TNT blast correlations to estimate overpressure.\n\n"
            "Characteristics:\n"
            "- Simple calculation\n"
            "- Minimal parameters\n"
            "- Commonly accepted across industries and regulators\n\n"
            "Limitations:\n"
            "- High explosives & Gas explosions have a different physical mechanism. Hence, this model is not fit for modelling intricate process facilities"
        ),
        "formula": "W = η × m × ΔHc / ΔHTNT, Ze = R / W^(1/3), Ps = 573 × Ze^-1.685 / 100",
        "form_class": TNTExplosionForm,
        "calculator": calculate_tnt_equivalency,
        "record_type": ExplosionCalculation.CalculationType.TNT,
        "result_label": "Ps",
        "unit": "bar",
        "primary_key": "peak_overpressure",
        "details": (
            ("tnt_equivalent_mass", "TNT mass"),
            ("scaled_distance", "Scaled distance"),
        ),
    },
    "tno": {
        "title": "TNO multi-energy",
        "help_text": (
            "Developed to elimitate TNT model's limitations and consider the more complex physical conditions of real-world process facilities\n"
            "\n"
            "Key findings incorporated into the model:\n"
            "- More obstables -> higher fire spread and exponential overpressure\n"
            "- Therefore, the explosion power not only depends on energy, but also the environment\n"
            "- Complexity quantified into an index between 1 and 10, 10 being the most complex\n"
        ),
        "formula": "E = m × LHV, R' = R / (E / p0 / 1000)^(1/3), Ps = 0.406 × R'^-1.2",
        "form_class": TNOExplosionForm,
        "calculator": calculate_tno_overpressure,
        "record_type": ExplosionCalculation.CalculationType.TNO,
        "result_label": "Ps",
        "unit": "bar",
        "primary_key": "peak_overpressure",
        "details": (
            ("energy_kj", "Energy"),
            ("scaled_distance", "Scaled distance"),
        ),
    },
    "bst": {
        "title": "BST blast curve",
        "help_text": (
            "Uses the Baker-Strehlow-Tang correlation to estimate overpressure from scaled distance and explosion energy.\n"
        ),
        "formula": "R' = R / (E / p0 / 1000)^(1/3), Ps = 0.085 × R'^-1.05",
        "form_class": BSTExplosionForm,
        "calculator": calculate_bst_overpressure,
        "record_type": ExplosionCalculation.CalculationType.BST,
        "result_label": "Ps",
        "unit": "bar",
        "primary_key": "peak_overpressure",
        "details": (
            ("energy_kj", "Energy"),
            ("scaled_distance", "Scaled distance"),
        ),
    },
}


def _build_forms(post_data=None, submitted_panel=None):
    forms = {}
    for panel_key, config in EXPLOSION_PANEL_CONFIG.items():
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


def explosion_dashboard(request):
    selected_panel = "tnt"
    forms = _build_forms()
    panel_results = {}

    if request.method == "POST":
        selected_panel = request.POST.get("calculator", selected_panel)
        forms = _build_forms(request.POST, selected_panel)

        if selected_panel in EXPLOSION_PANEL_CONFIG:
            form = forms[selected_panel]
            panel = EXPLOSION_PANEL_CONFIG[selected_panel]
            if form.is_valid():
                inputs = dict(form.cleaned_data)
                result = panel["calculator"](**inputs)
                ExplosionCalculation.objects.create(
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

    recent_calculations = ExplosionCalculation.objects.all()[:8]
    panel_cards = []
    for panel_key, panel in EXPLOSION_PANEL_CONFIG.items():
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
            "eyebrow": "Consequence Demo / Explosion",
            "title": "Explosion Calculators",
            "description": "Compare TNT, TNO, and BST explosion models against the underlying blast scripts and keep a saved history of overpressure checks.",
            "history_copy": "Saved TNT, TNO, and BST overpressure runs from the explosion workspace.",
            "accent": "#6b3f9c",
            "accent_deep": "#4d2c72",
            "accent_soft": "rgba(107, 63, 156, 0.14)",
            "empty_copy": "No explosion calculations saved yet.",
        },
        "panel_cards": panel_cards,
        "recent_calculations": recent_calculations,
        "selected_panel": selected_panel,
        "clear_url_name": "clear_explosion_history",
    }
    return render(request, "consequence/dashboard.html", context)


@require_POST
def clear_explosion_history(request):
    ExplosionCalculation.objects.all().delete()
    return redirect("explosion_dashboard")
