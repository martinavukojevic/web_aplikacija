# Generated by Django 4.2.13 on 2024-06-12 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aplikacija", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="korisnik",
            old_name="roles",
            new_name="role",
        ),
    ]
