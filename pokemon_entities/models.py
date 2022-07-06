from xml.dom.minidom import Element
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Имя покемона')
    title_en = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на английском',
        blank=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Имя покемона на японском',
        blank=True,
    )
    previous_evolution = models.ForeignKey(
        "self",
        related_name='next_evolutions',
        verbose_name='Из какого покемона эволюционировал',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(default='default_pokemon_emage.png')
    description = models.TextField(blank=True)
    element_type = models.ManyToManyField(
        'PokemonElementType',
        related_name='pokemons',
    )

    def display_evolution(self):
        if self.previous_evolution:
            return f'Эволюционировал из {self.previous_evolution.title}'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pokemon', args=[str(self.id)])




class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_location',
        verbose_name='покемон',
    )
    lat = models.FloatField(verbose_name='Широта в местоположении')
    lon = models.FloatField(verbose_name='Долгота в местоположении')
    appeared_at = models.DateTimeField(
        verbose_name='Когда покемон появится на карте',
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Когда покемон исчезнет с карты',
    )
    level = models.IntegerField(
        verbose_name='Уровень покемона',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    health = models.IntegerField(
        verbose_name='Здоровье покемона',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    strength = models.IntegerField(
        verbose_name='Сила покемона',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    defence = models.IntegerField(
        verbose_name='Броня покемона',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость покемона',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )


class PokemonElementType(models.Model):
    WT = 'WATER'
    FR = 'FIRE'
    GR = 'GRASS'
    EL = 'ELECTRO'
    MG = 'MAGICAL'
    ICE = 'ICE'
    ELEMET_CHOICES = (
        (WT, 'Water'),
        (FR, 'Fire'),
        (GR, 'Grass'),
        (EL, 'Electro'),
        (MG, 'Magical'),
        (ICE, 'Ice'),
    )
    title = models.CharField(
        max_length=20,
        choices=ELEMET_CHOICES,
        unique=True,
    )
