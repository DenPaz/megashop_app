from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.core.viewmixins import HtmxTemplateMixin
from apps.orders.models import Order
from apps.orders.models import OrderItem

from .forms import AddressForm
from .forms import PersonalInfoForm


class PersonalInfoUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    form_class = PersonalInfoForm
    template_name = "accounts/personal_info_update.html"
    success_url = reverse_lazy("accounts:personal_info_update")
    success_message = _("Informações pessoais atualizadas com sucesso.")

    def get_object(self, queryset=None):
        return self.request.user


class AddressUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    form_class = AddressForm
    template_name = "accounts/address_update.html"
    success_url = reverse_lazy("accounts:address_update")
    success_message = _("Endereço atualizado com sucesso.")

    def get_object(self, queryset=None):
        return self.request.user.profile


class PasswordUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    AllauthPasswordChangeView,
):
    template_name = "accounts/password_update.html"
    success_url = reverse_lazy("accounts:password_update")
    success_message = _("Senha atualizada com sucesso.")


class OrderListView(
    HtmxTemplateMixin,
    LoginRequiredMixin,
    ListView,
):
    model = Order
    template_name = "accounts/order_list.html"
    htmx_template_name = "accounts/partials/order_list_table.html"
    context_object_name = "orders"
    paginate_by = 7

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=OrderItem.objects.select_related("product"),
                ),
            )
        )
