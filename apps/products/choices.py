from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.TextChoices):
    ELECTRONICS = "ELECTRONICS", _("Electrônicos")
    FASHION = "FASHION", _("Moda")
    HOME = "HOME", _("Casa")
    BEAUTY = "BEAUTY", _("Beleza")
    SPORTS = "SPORTS", _("Esportes")
    TOYS = "TOYS", _("Brinquedos")
    BOOKS = "BOOKS", _("Livros")
    MUSIC = "MUSIC", _("Música")
    GROCERY = "GROCERY", _("Mercearia")
    AUTOMOTIVE = "AUTOMOTIVE", _("Automotivo")
    HEALTH = "HEALTH", _("Saúde")
    OFFICE = "OFFICE", _("Escritório")
    PETS = "PETS", _("Animais de Estimação")
    BABY = "BABY", _("Bebê")
    GARDEN = "GARDEN", _("Jardim")
    TOOLS = "TOOLS", _("Ferramentas")
    JEWELRY = "JEWELRY", _("Joias")
    OTHER = "OTHER", _("Outros")
