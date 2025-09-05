from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code="password_no_upper",
            )

    def get_error_message(self):
        return _("A senha não contém letras maiúsculas.")

    def get_help_text(self):
        return _("A senha deve conter pelo menos uma letra maiúscula.")


class LowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                self.get_error_message(),
                code="password_no_lower",
            )

    def get_error_message(self):
        return _("A senha não contém letras minúsculas.")

    def get_help_text(self):
        return _("A senha deve conter pelo menos uma letra minúscula.")
