from operator import mod
from statistics import mode
from django.db import models

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
    latitude = models.FloatField()
    longitude = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
