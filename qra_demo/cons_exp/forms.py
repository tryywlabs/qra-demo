from django import forms


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


class TNTExplosionForm(PanelForm):
    efficiency = forms.FloatField(
        min_value=0,
        max_value=1,
        label="Explosion efficiency",
        initial=0.06,
    )
    mass_kg = forms.FloatField(
        min_value=0.0001,
        label="Participating mass (kg)",
        initial=120.0,
    )
    heat_combustion_kj_kg = forms.FloatField(
        min_value=0.0001,
        label="Heat of combustion (kJ/kg)",
        initial=50000.0,
    )
    tnt_heat_combustion_kj_kg = forms.FloatField(
        min_value=0.0001,
        label="TNT heat of combustion (kJ/kg)",
        initial=4680.0,
    )
    distance_m = forms.FloatField(
        min_value=0.0001,
        label="Stand-off distance (m)",
        initial=25.0,
    )


class TNOExplosionForm(PanelForm):
    mass_participating_kg = forms.FloatField(
        min_value=0.0001,
        label="Participating mass (kg)",
        initial=150.0,
    )
    lower_heating_value_kj_kg = forms.FloatField(
        min_value=0.0001,
        label="Lower heating value (kJ/kg)",
        initial=50000.0,
    )
    ambient_pressure_pa = forms.FloatField(
        min_value=0.0001,
        label="Ambient pressure (Pa)",
        initial=101325.0,
    )
    distance_m = forms.FloatField(
        min_value=0.0001,
        label="Stand-off distance (m)",
        initial=25.0,
    )


class BSTExplosionForm(PanelForm):
    energy_kj = forms.FloatField(
        min_value=0.0001,
        label="Explosion energy (kJ)",
        initial=750000.0,
    )
    ambient_pressure_pa = forms.FloatField(
        min_value=0.0001,
        label="Ambient pressure (Pa)",
        initial=101325.0,
    )
    distance_m = forms.FloatField(
        min_value=0.0001,
        label="Stand-off distance (m)",
        initial=25.0,
    )
