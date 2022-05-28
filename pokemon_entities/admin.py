from dataclasses import field
from .models import Pokemon, PokemonEntity
from django.contrib import admin


@admin.register(Pokemon)
class AdminPokemon(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(PokemonEntity)
class AdminEntity(admin.ModelAdmin):
    list_display = ('latitude', 'longitude')