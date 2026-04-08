from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cons_gas", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
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
                    options={
                        "ordering": ["-created_at"],
                        "db_table": "cons_gas_explosioncalculation",
                    },
                ),
            ],
        ),
    ]
