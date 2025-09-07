from allauth.account.views import PasswordChangeView as AllauthPasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView

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
