import uuid

from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import formats
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from apps.core.utils import get_default_product_image_url
from apps.core.validators import FileSizeValidator

from .choices import Category


class Product(TimeStampedModel):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("Nome"),
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        max_length=220,
        unique=True,
    )
    category = models.CharField(
        verbose_name=_("Departamento"),
        max_length=50,
        choices=Category.choices,
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        blank=True,
    )
    price = models.DecimalField(
        verbose_name=_("Preço"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text=_("Preço em BRL"),
    )
    stock = models.PositiveIntegerField(
        verbose_name=_("Estoque"),
        validators=[MinValueValidator(0)],
        default=0,
        help_text=_("Estoque disponível"),
    )
    image = models.ImageField(
        verbose_name=_("Imagem"),
        upload_to="products/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            FileSizeValidator(max_size=5 * 1024 * 1024),  # 5 MB
        ],
        blank=True,
        help_text=_("Tamanho máximo: 5MB. Formatos permitidos: JPG, JPEG, PNG."),
    )

    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name}"

    def get_price_display(self):
        return f"R$ {formats.number_format(self.price, 2)}"

    def get_product_image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return get_default_product_image_url()

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})
