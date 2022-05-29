from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        null=True,
        blank=True,
    )
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_location'
    )
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
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
