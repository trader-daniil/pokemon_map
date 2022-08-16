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
    image = models.ImageField(verbose_name='Изображение покемона')
    description = models.TextField(
        blank=True,
        verbose_name='Описание покемона',
    )
    element_type = models.ManyToManyField(
        'PokemonElementType',
        related_name='pokemons',
        verbose_name='Стихии покемона',
    )

    def clean(self):
        if self.element_type and self.element_type.count() > 3:
            max_elements = list(self.element_type.all()[:3])
            self.element_type.clear()
            self.element_type.set(max_elements)

    def display_previous_evolution(self):
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
        related_name='entities',
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
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    health = models.IntegerField(
        verbose_name='Здоровье покемона',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    strength = models.IntegerField(
        verbose_name='Сила покемона',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    defence = models.IntegerField(
        verbose_name='Броня покемона',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость покемона',
        validators=[MinValueValidator(0)],
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
    TX = 'TOXIC'
    ST = 'STONE'
    ELEMET_CHOICES = (
        (WT, 'Water'),
        (FR, 'Fire'),
        (GR, 'Grass'),
        (EL, 'Electro'),
        (MG, 'Magical'),
        (ICE, 'Ice'),
        (TX, 'Toxic'),
        (ST, 'Stone'),
    )
    title = models.CharField(
        max_length=20,
        choices=ELEMET_CHOICES,
        unique=True,
        verbose_name='Название стихии',
    )
    image = models.ImageField(verbose_name='Изображение стихии')
    strong_against = models.ManyToManyField(
        'self',
        symmetrical=False,
        verbose_name='Более слабые стихии',
    )
