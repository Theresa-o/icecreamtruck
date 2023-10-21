# Generated by Django 4.2.6 on 2023-10-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("icecreamapi", "0002_transaction"),
    ]

    operations = [
        migrations.CreateModel(
            name="Earnings",
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
                (
                    "total_earnings",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
            ],
        ),
    ]