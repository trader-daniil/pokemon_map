import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_datetime = localtime()
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(
        location=MOSCOW_CENTER,
        zoom_start=12,
    )
    pokemons_on_map = PokemonEntity.objects.select_related('pokemon').filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime,
    )
    for pokemon_entity in pokemons_on_map:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.lat,
            lon=pokemon_entity.lon,
            image_url=pokemon_entity.pokemon.image.path,
        )
    pokemons_on_page = []
    for pokemon in pokemons:
        try:
            pokemon_image_path = pokemon.image.url
        except ValueError:
            pokemon_image_path = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_path,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound(
            f'<h1>Покемон с индеком {pokemon_id} не найден</h1>',
        )
    folium_map = folium.Map(
        location=MOSCOW_CENTER,
        zoom_start=12,
    )
    current_datetime = localtime()
    pokemons_on_map = requested_pokemon.entities.filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime,
    )
    for pokemon_entity in pokemons_on_map:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.lat,
            lon=pokemon_entity.lon,
            image_url=requested_pokemon.image.path,
        )

    pokemon_previous_evolution = {}
    pokemon_next_evolution = {}
    pokemon_elemetns = []

    """Добавление покемона, в которого эволюционирует"""
    if requested_pokemon.next_evolutions.first():
        pokemon_evolutioned = requested_pokemon.next_evolutions.first()
        pokemon_next_evolution = {
            'title_ru': pokemon_evolutioned.title,
            'pokemon_id': pokemon_evolutioned.id,
            'img_url': pokemon_evolutioned.image.url,
        }

    """Добавление покемона, из которого эволюционирует"""
    if requested_pokemon.previous_evolution:
        evolutioned_from_pokemon = requested_pokemon.previous_evolution
        pokemon_previous_evolution = {
            'title_ru': evolutioned_from_pokemon.title,
            'pokemon_id': evolutioned_from_pokemon.id,
            'img_url': evolutioned_from_pokemon.image.url,
        }

    """Добавление стихий покемона"""
    if requested_pokemon.element_type.all():
        requested_pokemon.clean()
        for element in requested_pokemon.element_type.all():
            serialized_strong_against_elements = []
            for weaker_element in element.strong_against.all():
                serialized_strong_against_elements.append(weaker_element.title)
            serialized_element = {
                'title': element.title,
                'img': element.image.url,
                'strong_against': serialized_strong_against_elements,
            }
            pokemon_elemetns.append(serialized_element)

    serialized_pokemon = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': requested_pokemon.image.url,
        'description': requested_pokemon.description,
        'next_evolution': pokemon_next_evolution,
        'previous_evolution': pokemon_previous_evolution,
        'element_type': pokemon_elemetns,
    }
    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': serialized_pokemon,
        },
    )
