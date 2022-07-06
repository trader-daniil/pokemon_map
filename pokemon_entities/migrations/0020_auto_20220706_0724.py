from ast import Add
from django.db import migrations

def add_element_to_pokemon(apps, schema_editor):
    Pokemon = apps.get_model('pokemon_entities', 'Pokemon')
    Element = apps.get_model('pokemon_entities', 'PokemonElementType')
    pokemons = Pokemon.objects.filter(element_type__isnull=True)
    element  = Element.objects.first()
    for pokemon in pokemons:
        pokemon.element_type.add(element)
        pokemon.save()
        


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0019_auto_20220705_1832'),
    ]

    operations = [
        migrations.RunPython(add_element_to_pokemon),
    ]
