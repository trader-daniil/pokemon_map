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
    pokemons_in_db = Pokemon.objects.all()
    folium_map = folium.Map(
        location=MOSCOW_CENTER,
        zoom_start=12,
    )
    for pokemon in pokemons_in_db:
        pokemons_on_map = PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lte=current_datetime,
            disappeared_at__gte=current_datetime,
        )
        for pokemon_entity in pokemons_on_map:
            add_pokemon(
                folium_map=folium_map,
                lat=pokemon_entity.lat,
                lon=pokemon_entity.lon,
                image_url=pokemon.image.path,
            )
    pokemons_on_page = []
    for pokemon in pokemons_in_db:
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
    pokemons_on_map = PokemonEntity.objects.filter(
            pokemon=requested_pokemon,
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
    if requested_pokemon.next_evolutions.first():
        pokemon_evolutioned = requested_pokemon.next_evolutions.first()
        pokemon_next_evolution['title_ru'] = pokemon_evolutioned.title
        pokemon_next_evolution['pokemon_id'] = pokemon_evolutioned.id
        pokemon_next_evolution['img_url'] = pokemon_evolutioned.image.url
    if requested_pokemon.previous_evolution:
        evolutioned_from_pokemon = requested_pokemon.previous_evolution
        pokemon_previous_evolution['title_ru'] = evolutioned_from_pokemon.title
        pokemon_previous_evolution['pokemon_id'] = evolutioned_from_pokemon.id
        pokemon_image_url = evolutioned_from_pokemon.image.url
        pokemon_previous_evolution['img_url'] = pokemon_image_url

    pokemon_info = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'img_url': requested_pokemon.image.url,
        'description': requested_pokemon.description,
        'next_evolution': pokemon_next_evolution,
        'previous_evolution': pokemon_previous_evolution,
    }
    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon_info,
        },
    )
