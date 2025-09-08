from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    OPEN = "OPEN", _("Aberto")
    PAID = "PAID", _("Pago")
    CANCELLED = "CANCELLED", _("Cancelado")
