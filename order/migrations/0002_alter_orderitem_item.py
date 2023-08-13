# Generated by Django 4.1.5 on 2023-08-13 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_productimages_alt_text"),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_items",
                to="store.product",
            ),
        ),
    ]
