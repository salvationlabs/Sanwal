# Generated by Django 4.1.5 on 2023-06-28 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BillingAddress",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="Last Name"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=15, verbose_name="Phone Number"),
                ),
                (
                    "address_line_1",
                    models.CharField(max_length=150, verbose_name="Address Line 1"),
                ),
                (
                    "address_line_2",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Address Line 1"
                    ),
                ),
                ("city", models.CharField(max_length=150, verbose_name="City")),
                (
                    "state",
                    models.CharField(
                        max_length=150, verbose_name="State/Province/Region"
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        max_length=2, verbose_name="Country"
                    ),
                ),
                ("zip_code", models.CharField(max_length=12, verbose_name="Zip Code")),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Customer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Billing Address",
                "verbose_name_plural": "Billing Addresses",
            },
        ),
    ]
