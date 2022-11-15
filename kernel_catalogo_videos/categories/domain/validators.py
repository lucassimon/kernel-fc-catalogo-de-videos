"""
Define um ou mais validators para categoria
"""

# Python

# Third
from kernel_catalogo_videos.core.domain.validators import PropsValidated, ValidatorFieldInterface

# Apps


class DummyValidator(ValidatorFieldInterface[PropsValidated]):
    """
    Validação de serializers do django rest framework
    """

    def validate(self, is_valid: bool) -> bool:
        if not is_valid:
            return False

        return True
