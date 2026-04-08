from django import forms


STABILITY_CLASS_CHOICES = [(code, code) for code in "ABCDEF"]


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


class GasPlumeForm(PanelForm):
    release_rate_kg_s = forms.FloatField(
        min_value=0.0001,
        label="Release rate (kg/s)",
        initial=1.2,
    )
    wind_speed_m_s = forms.FloatField(
        min_value=0.0001,
        label="Wind speed (m/s)",
        initial=5.0,
    )
    release_height_m = forms.FloatField(
        min_value=0,
        label="Release height (m)",
        initial=2.0,
    )
    downwind_distance_m = forms.FloatField(
        min_value=0.0001,
        label="Downwind distance x (m)",
        initial=100.0,
    )
    crosswind_distance_m = forms.FloatField(
        min_value=0,
        label="Crosswind distance y (m)",
        initial=0.0,
    )
    receptor_height_m = forms.FloatField(
        min_value=0,
        label="Receptor height z (m)",
        initial=1.5,
    )
    stability_class = forms.ChoiceField(
        choices=STABILITY_CLASS_CHOICES,
        label="Stability class",
        initial="D",
    )


class GasPuffForm(PanelForm):
    released_mass_kg = forms.FloatField(
        min_value=0.0001,
        label="Released mass (kg)",
        initial=50.0,
    )
    release_height_m = forms.FloatField(
        min_value=0,
        label="Release height (m)",
        initial=2.0,
    )
    downwind_distance_m = forms.FloatField(
        min_value=0.0001,
        label="Downwind distance x (m)",
        initial=60.0,
    )
    crosswind_distance_m = forms.FloatField(
        min_value=0,
        label="Crosswind distance y (m)",
        initial=0.0,
    )
    receptor_height_m = forms.FloatField(
        min_value=0,
        label="Receptor height z (m)",
        initial=1.5,
    )
    stability_class = forms.ChoiceField(
        choices=STABILITY_CLASS_CHOICES,
        label="Stability class",
        initial="D",
    )
