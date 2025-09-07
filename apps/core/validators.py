from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:  # noqa: PLW1641
    message = _("O tamanho do arquivo não pode ser maior que %(max_size)d %(unit)s.")
    code = "max_size"
    units = {
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
    }

    def __init__(self, max_size, unit="MB"):
        if unit not in self.units:
            raise ValueError(_("Unidade '%(unit)s' inválida.") % {"unit": unit})
        self.max_size = max_size
        self.unit = unit

    def __call__(self, value):
        max_size_bytes = self.max_size * self.units[self.unit]
        if value.size > max_size_bytes:
            raise ValidationError(
                self.message,
                code=self.code,
                params={"max_size": self.max_size, "unit": self.unit},
            )

    def __eq__(self, other):
        return isinstance(other, FileSizeValidator) and vars(self) == vars(other)
