# Generated by Django 4.2.6 on 2023-10-26 01:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("icecreamapi", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="truck",
            name="sales",
            field=models.ManyToManyField(
                blank=True, related_name="trucks", to="icecreamapi.sale"
            ),
        ),
    ]