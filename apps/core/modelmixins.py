from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .choices import BrasilState
from .choices import Gender


class PersonalInfoMixin(models.Model):
    birth_date = models.DateField(
        verbose_name=_("Data de nascimento"),
        blank=True,
        null=True,
    )
    gender = models.CharField(
        verbose_name=_("Gênero"),
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Número de telefone"),
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            msg = _("A data de nascimento não pode ser no futuro.")
            raise ValidationError({"birth_date": msg})

    @property
    def age(self):
        if self.birth_date:
            today = timezone.now().date()
            age = relativedelta(today, self.birth_date)
            return age.years
        return None


class AddressMixin(models.Model):
    cep = models.CharField(
        verbose_name=_("CEP"),
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^\d{8}$",
                message=_("CEP deve conter 8 dígitos."),
                code="invalid_cep",
            ),
        ],
        blank=True,
    )
    state = models.CharField(
        verbose_name=_("Estado"),
        max_length=2,
        choices=BrasilState.choices,
        blank=True,
    )
    city = models.CharField(
        verbose_name=_("Cidade"),
        max_length=50,
        blank=True,
    )
    neighborhood = models.CharField(
        verbose_name=_("Bairro"),
        max_length=50,
        blank=True,
    )
    street = models.CharField(
        verbose_name=_("Logradouro"),
        max_length=50,
        blank=True,
    )
    number = models.CharField(
        verbose_name=_("Número"),
        max_length=10,
        blank=True,
    )
    complement = models.CharField(
        verbose_name=_("Complemento"),
        max_length=50,
        blank=True,
    )

    class Meta:
        abstract = True

    @property
    def formatted_cep(self):
        return f"{self.cep[:5]}-{self.cep[5:]}" if self.cep else ""

    @property
    def full_address(self):
        parts = [
            self.street,
            self.number,
            self.complement,
            self.neighborhood,
            self.city,
            self.state,
            self.formatted_cep,
        ]
        return ", ".join(filter(None, parts))
