from django.test import TestCase, Client
from django.urls import reverse

from pokemon_entities.models import Pokemon

POKEMON_NAME = 'Пикачу'
HOMEPAGE = reverse('mainpage')
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


class PokemonTestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pokemon = Pokemon.objects.create(
            title='Покемон_для_теста',
            title_en='Pokemon_for_test',
            description='Description of pokemon',
            image=DEFAULT_IMAGE_URL,
        )
        cls.pokemon_2 = Pokemon.objects.create(
            previous_evolution=cls.pokemon,
            title='Покемон_для_теста_2',
            title_en='Pokemon_for_test_2',
            description='Description of pokemon 2',
            image=DEFAULT_IMAGE_URL,
        )
        cls.guest_client = Client()
        cls.POKEMON_ID_URL = reverse(
            'pokemon',
            args=[
                cls.pokemon.id
            ],
        )

    def test_pages_context(self):
        guest_client = PokemonTestViews.guest_client
        pokemon = PokemonTestViews.pokemon
        pokemon_2 = PokemonTestViews.pokemon_2
        pokemon_data = {
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        }
        pokemon_2_data = {
            'title_ru': pokemon_2.title,
            'pokemon_id': pokemon_2.id,
            'img_url': pokemon_2.image.url,
        }
        response_main_page = guest_client.get(HOMEPAGE)
        self.assertIn(
            pokemon_data,
            response_main_page.context['pokemons'],
        )
        self.assertIn(
            pokemon_2_data,
            response_main_page.context['pokemons'],
        )
        pokemon_info = {
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': '',
            'img_url': pokemon.image.url,
            'description': pokemon.description,
            'next_evolution': pokemon_2_data,
            'previous_evolution': {},
        }
        response_pokemon_page = guest_client.get(self.POKEMON_ID_URL)
        self.assertEqual(
            pokemon_info,
            response_pokemon_page.context['pokemon'],
        )
