# Generated by Django 3.1.14 on 2022-06-30 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_auto_20220630_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
    ]
