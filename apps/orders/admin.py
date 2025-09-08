from django.contrib import admin
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from .models import Order
from .models import OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1
    verbose_name = _("Item")
    verbose_name_plural = _("Itens")
    autocomplete_fields = ["product"]
    fields = (
        "product",
        "quantity",
        "inline_subtotal",
    )
    readonly_fields = ("inline_subtotal",)

    def inline_subtotal(self, obj):
        if not obj.pk:
            return "-"
        total = 0.00
        if obj.product:
            total = obj.product.price * obj.quantity
        return f"R$ {formats.number_format(total, 2)}"

    inline_subtotal.short_description = _("Subtotal")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Informações do pedido"),
            {
                "fields": (
                    "user",
                    "status",
                ),
            },
        ),
        (
            _("Datas importantes"),
            {
                "fields": (
                    "created",
                    "modified",
                ),
            },
        ),
        (
            _("Resumo"),
            {
                "fields": (
                    "total_amount",
                    "number_of_items",
                ),
            },
        ),
    )
    list_display = (
        "short_id",
        "user",
        "status",
        "created",
        "total_amount",
        "number_of_items",
    )
    list_filter = [
        "status",
    ]
    date_hierarchy = "created"
    search_fields = [
        "id",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    autocomplete_fields = ["user"]
    readonly_fields = [
        "created",
        "modified",
        "total_amount",
        "number_of_items",
    ]
    inlines = (OrderItemInline,)

    def short_id(self, obj):
        return str(obj.id)[:8]
