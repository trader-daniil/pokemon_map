# Generated by Django 4.0.6 on 2022-08-15 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0027_alter_pokemonentity_pokemon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='image',
            field=models.ImageField(default='\\media\\water.webp', upload_to='', verbose_name='Изображение стихии'),
            preserve_default=False,
        ),
    ]
