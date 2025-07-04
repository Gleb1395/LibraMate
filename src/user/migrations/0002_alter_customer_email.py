# Generated by Django 5.2 on 2025-04-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with that email already exists."},
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
    ]
