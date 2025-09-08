import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from .choices import OrderStatus

User = get_user_model()


class Order(TimeStampedModel):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        to=User,
        verbose_name=_("Usuário"),
        related_name="orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.OPEN,
        db_index=True,
    )

    class Meta:
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")
        ordering = ["-created"]

    def __str__(self):
        return f"Pedido #{str(self.id)[:8]}"

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"pk": self.pk})

    @property
    def total_amount(self):
        return sum(item.subtotal_amount for item in self.items.all())

    def get_total_amount_display(self):
        return f"R$ {self.total_amount:.2f}".replace(".", ",")

    @property
    def number_of_items(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(TimeStampedModel):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    order = models.ForeignKey(
        to=Order,
        verbose_name=_("Pedido"),
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to="products.Product",
        verbose_name=_("Produto"),
        related_name="order_items",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantidade"),
        validators=[MinValueValidator(1)],
        default=1,
    )

    class Meta:
        verbose_name = _("Item do pedido")
        verbose_name_plural = _("Itens do pedido")
        ordering = ["-created"]
        unique_together = ("order", "product")

    def __str__(self):
        name = self.product.name if self.product else _("Produto removido")
        return f"Pedido #{str(self.order.id)[:8]} - {name} (x{self.quantity})"

    @property
    def subtotal_amount(self):
        if not self.product:
            return 0.00
        return self.product.price * self.quantity
