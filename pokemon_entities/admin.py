from dataclasses import field
from .models import Pokemon, PokemonEntity
from django.contrib import admin


@admin.register(Pokemon)
class AdminPokemon(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'title_en',
        'title_jp',
    )


@admin.register(PokemonEntity)
class AdminEntity(admin.ModelAdmin):
    list_display = (
        'lat',
        'lon',
        'appeared_at',
        'disappeared_at',
    )