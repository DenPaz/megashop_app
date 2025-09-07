from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Profile
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            _("Informações de login"),
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Informações pessoais"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Permissões"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Datas importantes"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    list_filter = [
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    filter_horizontal = [
        "groups",
        "user_permissions",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "email",
    ]
    ordering = [
        "first_name",
        "last_name",
    ]
    readonly_fields = [
        "last_login",
        "date_joined",
    ]
    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Informações pessoais"),
            {
                "fields": (
                    "user",
                    "profile_picture",
                    "birth_date",
                    "gender",
                    "phone_number",
                ),
            },
        ),
        (
            _("Endereço"),
            {
                "fields": (
                    "cep",
                    "state",
                    "city",
                    "neighborhood",
                    "street",
                    "number",
                    "complement",
                ),
            },
        ),
    )
    list_display = [
        "user",
        "phone_number",
    ]
    list_filter = [
        "user__is_active",
    ]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    readonly_fields = [
        "user",
    ]
    list_per_page = 10
