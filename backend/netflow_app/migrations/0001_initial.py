# Generated by Django 4.2.2 on 2023-06-18 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Node",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("SUP", "Supply"),
                            ("DEM", "Demand"),
                            ("STO", "Storage"),
                        ],
                        max_length=3,
                    ),
                ),
            ],
        ),
    ]
