from django.test import TestCase
from datetime import datetime, timedelta
from pokemon_entities.models import Pokemon, PokemonEntity


class TestPokemonModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pokemon = Pokemon.objects.create(
            title='Покемон_для_теста',
            title_en='Pokemon_for_test',
            description='Description of pokemon',
        )
        cls.pokemonentity = PokemonEntity(
            pokemon=cls.pokemon,
            lat=55.730141,
            lon=37.653911,
            appeared_at=datetime.today(),
            disappeared_at=datetime.today() + timedelta(days=1),
            health=4,
            strength=6,
            defence=8,
            stamina=10,
        )

    def test_pokemon_values(self):
        pokemon_fields_values = {
            'title': 'Покемон_для_теста',
            'title_en': 'Pokemon_for_test',
            'title_jp': None,
            'description': 'Description of pokemon',
        }
        pokemon = TestPokemonModel.pokemon
        for field, expected_value in pokemon_fields_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(
                        pokemon,
                        field,
                    ),
                    expected_value,
                )

    def test_pokemon_entities(self):
        entity_fields_values = {
            'lat': 55.730141,
            'lon': 37.653911,
            'health': 4,
            'strength': 6,
            'defence': 8,
            'stamina': 10,
        }
        pokemon = TestPokemonModel.pokemon
        pokemon_entity = TestPokemonModel.pokemonentity
        self.assertTrue(pokemon_entity.pokemon == pokemon)
        for field, expected_value in entity_fields_values.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(
                        pokemon_entity,
                        field,
                    ),
                    expected_value,
                )

    def test_verbose_names_pokemon(self):
        pokemon = TestPokemonModel.pokemon
        pokemon_fields_verbose = {
            'title': 'Имя покемона',
            'title_en': 'Имя покемона на английском',
            'title_jp': 'Имя покемона на японском',
            'previous_evolution': 'Из какого покемона эволюционировал',

        }
        for field, expected_value in pokemon_fields_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    pokemon._meta.get_field(field).verbose_name,
                    expected_value,
                )

    def test_verbose_names_pokemon_entity(self):
        pokemon_emtity = TestPokemonModel.pokemonentity
        entity_fields_verbose = {
            'pokemon': 'покемон',
            'lat': 'Широта в местоположении',
            'lon': 'Долгота в местоположении',
            'appeared_at': 'Когда покемон появится на карте',
            'disappeared_at': 'Когда покемон исчезнет с карты',
            'level': 'Уровень покемона',
            'health': 'Здоровье покемона',
            'strength': 'Сила покемона',
            'defence': 'Броня покемона',
            'stamina': 'Выносливость покемона',
        }
        for field, expected_value in entity_fields_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    pokemon_emtity._meta.get_field(field).verbose_name,
                    expected_value,
                )
