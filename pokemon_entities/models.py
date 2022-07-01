from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='pokemon name')
    title_en = models.CharField(
        max_length=200,
        verbose_name='pokemon name in english')
    title_jp = models.CharField(
        max_length=200,
        verbose_name='pokemon name in japanese')
    previous_evolution = models.ForeignKey(
        "self",
        related_name='next_evolutions',
        verbose_name='from whom pokemon evolved',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    def display_evolution(self):
        if self.previous_evolution:
            return f'Эволюционировал из {self.previous_evolution.title}'

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_location'
    )
    lat = models.FloatField(verbose_name='latitude of location')
    lon = models.FloatField(verbose_name='longitude of location')
    appeared_at = models.DateTimeField(
        verbose_name='when pokemon emerge on map',
    )
    disappeared_at = models.DateTimeField(
        verbose_name='when pokemon disappeared from map',
    )
    level = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    health = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    strength = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    defence = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
    stamina = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )
