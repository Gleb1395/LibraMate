# Generated by Django 4.2 on 2025-04-11 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={
                "ordering": ["title"],
                "verbose_name": "Book",
                "verbose_name_plural": "Books",
            },
        ),
    ]
