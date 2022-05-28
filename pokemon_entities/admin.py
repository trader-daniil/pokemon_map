from dataclasses import field
from .models import Pokemon
from django.contrib import admin


@admin.register(Pokemon)
class AdminPokemon(admin.ModelAdmin):
    list_display = ('id', 'title')