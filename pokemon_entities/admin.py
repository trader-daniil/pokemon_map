from .models import Pokemon, PokemonEntity, PokemonElementType
from django.contrib import admin


@admin.register(Pokemon)
class AdminPokemon(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'title_en',
        'title_jp',
        'display_next_evolution',
    )


@admin.register(PokemonEntity)
class AdminEntity(admin.ModelAdmin):
    list_display = (
        'lat',
        'lon',
        'appeared_at',
        'disappeared_at',
    )

@admin.register(PokemonElementType)
class AdminElement(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
    
