# Generated by Django 4.2.6 on 2023-10-22 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("icecreamapi", "0004_transaction_earnings"),
    ]

    operations = [
        migrations.AddField(
            model_name="fooditem",
            name="image",
            field=models.ImageField(
                default="images/minticecream.jpg", upload_to="images/"
            ),
            preserve_default=False,
        ),
    ]
