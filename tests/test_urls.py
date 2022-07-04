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


class PokemonUrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pokemon = Pokemon.objects.create(
            title='Покемон_для_теста',
            title_en='Pokemon_for_test',
            description='Description of pokemon',
            image=DEFAULT_IMAGE_URL,
        )
        cls.guest_client = Client()
        cls.POKEMON_ID_URL = reverse(
            'pokemon',
            args=[
                cls.pokemon.id
            ],
        )

    def test_url_exists_at_desired_location(self):
        guest_client = PokemonUrlTest.guest_client
        app_urls = [
            [
                guest_client,
                HOMEPAGE,
                200,
            ],
            [
                guest_client,
                self.POKEMON_ID_URL,
                200,
            ],
        ]
        for client, url, status in app_urls:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, status)

    def test_template(self):
        guest_client = PokemonUrlTest.guest_client
        templates_urls = [
            [
                HOMEPAGE,
                'mainpage.html',
            ],
            [
                self.POKEMON_ID_URL,
                'pokemon.html',
            ],
        ]
        for url, template in templates_urls:
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    guest_client.get(url),
                    template,
                )
