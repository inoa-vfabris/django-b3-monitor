from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from validate_docbr import CPF


@deconstructible
class CpfValidator:
    """Validator for the CPF document"""

    message = _("Invalid CPF")
    validator = CPF()

    def __call__(self, value):
        if not self.validator.validate(value):
            raise ValidationError(self.message, code="invalid")
