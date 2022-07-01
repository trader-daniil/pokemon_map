from django.db import migrations


def change_next_evol_to_previous(apps, schema_editor):
    Pokemon = apps.get_model('pokemon_entities', 'Pokemon')
    pokemons_with_evolution = Pokemon.objects.filter(
        next_evolution__isnull=False,
    )
    for pokemon in pokemons_with_evolution:
        ev_pokemon = pokemon.next_evolution
        ev_pokemon.previous_evolution = pokemon
        pokemon.next_evolution = None
        pokemon.save()
        ev_pokemon.save()


def change_backward(apps, schema_editor):
    Pokemon = apps.get_model('pokemon_entities', 'Pokemon')
    evolutioned_pokemons = Pokemon.objects.filter(
        previous_evolution__isnull=False,
    )
    for evolutioned_pokemon in evolutioned_pokemons:
        pokemon = evolutioned_pokemon.previous_evolution
        pokemon.next_evolution = evolutioned_pokemon
        evolutioned_pokemon.previous_evolution = None
        pokemon.save()
        evolutioned_pokemon.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20220629_2159'),
    ]

    operations = [
        migrations.RunPython(
            change_next_evol_to_previous,
            change_backward,
        ),
    ]
