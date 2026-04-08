from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cons_exp", "0001_initial"),
        ("cons_gas", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="ExplosionCalculation"),
            ],
        ),
    ]
