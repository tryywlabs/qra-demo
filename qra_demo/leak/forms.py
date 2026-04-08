from django import forms


class PanelForm(forms.Form):
    """Shared numeric styling for the leak calculator panels."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "panel-input",
                    "step": "any",
                    "autocomplete": "off",
                }
            )


class GasLeakForm(PanelForm):
    diameter_mm = forms.FloatField(
        min_value=0,
        label="Hole diameter (mm)",
        initial=25,
    )
    density_kg_m3 = forms.FloatField(
        min_value=0,
        label="Gas density (kg/m^3)",
        initial=1.8,
    )
    pressure_bar_gauge = forms.FloatField(
        min_value=0,
        label="Pressure (bar gauge)",
        initial=80,
    )


class LiquidLeakForm(PanelForm):
    diameter_mm = forms.FloatField(
        min_value=0,
        label="Hole diameter (mm)",
        initial=25,
    )
    density_kg_m3 = forms.FloatField(
        min_value=0,
        label="Liquid density (kg/m^3)",
        initial=850,
    )
    pressure_bar_gauge = forms.FloatField(
        min_value=0,
        label="Pressure (bar gauge)",
        initial=50,
    )


class TwoPhaseLeakForm(PanelForm):
    ratio_GOR = forms.FloatField(
        min_value=0,
        label="Gas-oil ratio",
        initial=3,
    )
    Q_g = forms.FloatField(
        min_value=0,
        label="Gas release rate Qg (kg/s)",
        initial=0.42,
    )
    Q_L = forms.FloatField(
        min_value=0,
        label="Liquid release rate QL (kg/s)",
        initial=2.75,
    )
