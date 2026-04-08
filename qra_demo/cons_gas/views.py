from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import GasPlumeForm, GasPuffForm
from .models import GasDispersionCalculation
from .services import calculate_gaussian_plume, calculate_gaussian_puff

GAS_DISPERSION_PANEL_CONFIG = {
    "plume": {
        "title": "Gaussian plume",
        "help_text": "Steady-state dispersion model for continuous releases, useful when wind and release conditions are treated as constant over time.",
        "formula": "C = Q / (2πuσyσz) × exp(-y² / 2σy²) × [exp(-(H-z)² / 2σz²) + exp(-(H+z)² / 2σz²)]",
        "form_class": GasPlumeForm,
        "calculator": calculate_gaussian_plume,
        "record_type": GasDispersionCalculation.CalculationType.PLUME,
        "result_label": "C",
        "unit": "kg/m^3",
        "primary_key": "concentration",
        "details": (
            ("sigma_y", "sigma_y"),
            ("sigma_z", "sigma_z"),
        ),
    },
    "puff": {
        "title": "Gaussian puff",
        "help_text": "Transient dispersion model for finite releases, useful when a fixed mass is released and the cloud moves and spreads downwind.",
        "formula": "C = Q / ((2π)^1.5 σy²σz) × exp(-0.5(y/σy)^2) × [exp(-0.5((z-H)/σz)^2) + exp(-0.5((z+H)/σz)^2)]",
        "form_class": GasPuffForm,
        "calculator": calculate_gaussian_puff,
        "record_type": GasDispersionCalculation.CalculationType.PUFF,
        "result_label": "C",
        "unit": "kg/m^3",
        "primary_key": "concentration",
        "details": (
            ("sigma_y", "sigma_y"),
            ("sigma_z", "sigma_z"),
        ),
    },
}


def _build_forms(panel_config, post_data=None, submitted_panel=None):
    forms = {}
    for panel_key, config in panel_config.items():
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


def _dashboard_response(request, *, panel_config, model, workspace, clear_url_name):
    selected_panel = next(iter(panel_config))
    forms = _build_forms(panel_config)
    panel_results = {}

    if request.method == "POST":
        selected_panel = request.POST.get("calculator", selected_panel)
        forms = _build_forms(panel_config, request.POST, selected_panel)

        if selected_panel in panel_config:
            form = forms[selected_panel]
            panel = panel_config[selected_panel]
            if form.is_valid():
                inputs = dict(form.cleaned_data)
                result = panel["calculator"](**inputs)
                model.objects.create(
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

    recent_calculations = model.objects.all()[:8]
    panel_cards = []
    for panel_key, panel in panel_config.items():
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
        "workspace": workspace,
        "panel_cards": panel_cards,
        "recent_calculations": recent_calculations,
        "selected_panel": selected_panel,
        "clear_url_name": clear_url_name,
    }
    return render(request, "consequence/dashboard.html", context)


def gas_dispersion_dashboard(request):
    workspace = {
        "eyebrow": "Consequence Demo / Gas Dispersion",
        "title": "Gas Dispersion Calculators",
        "description": "Run the Gaussian plume and Gaussian puff models against the gas-dispersion scripts and store each result for comparison.",
        "history_copy": "Saved plume and puff concentration runs from the gas dispersion workspace.",
        "accent": "#2c6b86",
        "accent_deep": "#1d4e62",
        "accent_soft": "rgba(44, 107, 134, 0.14)",
        "empty_copy": "No gas dispersion calculations saved yet.",
    }
    return _dashboard_response(
        request,
        panel_config=GAS_DISPERSION_PANEL_CONFIG,
        model=GasDispersionCalculation,
        workspace=workspace,
        clear_url_name="clear_gas_dispersion_history",
    )


@require_POST
def clear_gas_dispersion_history(request):
    GasDispersionCalculation.objects.all().delete()
    return redirect("gas_dispersion_dashboard")
