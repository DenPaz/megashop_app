from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": forms.EmailField}


class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    class Meta(admin_forms.AdminUserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}
        error_messages = {
            "email": {"unique": _("Esse e-mail já está em uso.")},
        }


class UserSignupForm(SignupForm):
    first_name = forms.CharField(
        label=_("Nome"),
        max_length=50,
        required=True,
    )
    last_name = forms.CharField(
        label=_("Sobrenome"),
        max_length=50,
        required=True,
    )
