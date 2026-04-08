from django import forms


FUEL_CHOICES = [
    ("LNG", "LNG"),
    ("LH2", "LH2"),
    ("Methanol", "Methanol"),
    ("NH3", "NH3"),
    ("Diesel", "Diesel"),
]


class PanelForm(forms.Form):
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


class PoolFireForm(PanelForm):
    fuel = forms.ChoiceField(
        choices=FUEL_CHOICES,
        label="Fuel",
        initial="LNG",
    )
    D = forms.FloatField(min_value=0.0001, label="Pool diameter D (m)", initial=30.0)
    U = forms.FloatField(min_value=0, label="Wind speed U (m/s)", initial=5.0)
    rho = forms.FloatField(min_value=0.0001, label="Air density rho (kg/m^3)", initial=1.205)
    g = forms.FloatField(min_value=0.0001, label="Gravity g (m/s^2)", initial=9.81)
    A = forms.FloatField(min_value=0.0001, label="Flame-length coefficient A", initial=55.0)
    p = forms.FloatField(label="Flame-length exponent p", initial=0.6666667)
    q = forms.FloatField(label="Wind exponent q", initial=-0.21)
    r = forms.FloatField(min_value=0.0001, label="r", initial=17.17)
    beta = forms.FloatField(min_value=0.0001, label="beta", initial=0.06)
    dHc = forms.FloatField(min_value=0.0001, label="Heat of combustion dHc (kJ/kg)", initial=50000.0)
    Ca = forms.FloatField(min_value=0.0001, label="Heat capacity Ca", initial=1.0)
    Ta = forms.FloatField(min_value=0.0001, label="Ambient temperature Ta (K)", initial=293.15)
    Emax = forms.FloatField(min_value=0.0001, label="Maximum emissive power Emax (kW/m^2)", initial=325.0)
    Dopt = forms.FloatField(min_value=0.0001, label="Optical diameter Dopt (m)", initial=13.8)
    k_m = forms.FloatField(min_value=0.0001, label="Extinction coefficient k_m", initial=130.0)
    Lb_factor = forms.FloatField(min_value=0.0001, label="Lower-zone length factor", initial=0.6)
    S = forms.FloatField(min_value=0.0001, label="Separation distance S (m)", initial=10.0)
    H_override = forms.FloatField(
        min_value=0.0001,
        required=False,
        label="Optional flame height override H (m)",
    )
