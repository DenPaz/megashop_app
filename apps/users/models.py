import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.modelmixins import AddressMixin
from apps.core.modelmixins import PersonalInfoMixin
from apps.core.utils import get_default_profile_picture_url
from apps.core.utils import get_user_upload_path
from apps.core.validators import FileSizeValidator

from .managers import UserManager


class User(AbstractUser):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(
        verbose_name=_("Nome"),
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name=_("Sobrenome"),
        max_length=50,
    )
    email = models.EmailField(
        verbose_name=_("E-mail"),
        unique=True,
    )
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"


class Profile(PersonalInfoMixin, AddressMixin, models.Model):
    user = models.OneToOneField(
        to=User,
        verbose_name=_("Usuário"),
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_picture = models.ImageField(
        verbose_name=_("Foto de perfil"),
        upload_to=get_user_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            FileSizeValidator(max_size=5, unit="MB"),
        ],
        blank=True,
        help_text=_("Tamanho máximo: 5MB. Formatos permitidos: JPG, JPEG, PNG."),
    )

    class Meta:
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfis")
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return f"{self.user}"

    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        return get_default_profile_picture_url()
