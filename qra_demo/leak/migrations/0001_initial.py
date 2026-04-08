from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LeakCalculation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("calculation_type", models.CharField(choices=[("gas", "Gas leak"), ("liquid", "Liquid leak"), ("two_phase", "Two-phase leak")], max_length=20)),
                ("inputs", models.JSONField(default=dict)),
                ("result", models.FloatField()),
                ("unit", models.CharField(default="kg/s", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
