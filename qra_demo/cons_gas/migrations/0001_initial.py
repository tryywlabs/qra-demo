from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExplosionCalculation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "calculation_type",
                    models.CharField(
                        choices=[
                            ("tnt", "TNT equivalency"),
                            ("tno", "TNO multi-energy"),
                            ("bst", "BST blast curve"),
                        ],
                        max_length=20,
                    ),
                ),
                ("inputs", models.JSONField(default=dict)),
                ("result", models.JSONField(default=dict)),
                ("unit", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="GasDispersionCalculation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "calculation_type",
                    models.CharField(
                        choices=[
                            ("plume", "Gas plume dispersion"),
                            ("puff", "Gas puff dispersion"),
                        ],
                        max_length=20,
                    ),
                ),
                ("inputs", models.JSONField(default=dict)),
                ("result", models.JSONField(default=dict)),
                ("unit", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
