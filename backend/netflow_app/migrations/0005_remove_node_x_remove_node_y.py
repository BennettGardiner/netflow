# Generated by Django 4.2.2 on 2023-06-27 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("netflow_app", "0004_arc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="node",
            name="x",
        ),
        migrations.RemoveField(
            model_name="node",
            name="y",
        ),
    ]
