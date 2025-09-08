from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Detalhes do produto"),
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "description",
                    "price",
                    "stock",
                    "image",
                ),
            },
        ),
        (
            _("Metadados"),
            {
                "fields": (
                    "created",
                    "modified",
                ),
            },
        ),
    )
    list_display = [
        "name",
        "category",
        "price",
        "stock",
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        "name",
    ]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = [
        "created",
        "modified",
    ]
    list_per_page = 10
