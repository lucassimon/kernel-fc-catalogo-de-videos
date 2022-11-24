# Python
from dataclasses import fields

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain import validators


@pytest.mark.unit
def test_raises_not_implemented_error():

    with pytest.raises(TypeError) as assert_error:
        validators.ValidatorFieldInterface()

    assert assert_error.value.args[0] == (
        "Can't instantiate abstract class "
        "ValidatorFieldInterface with abstract "
        "method validate"
    )


@pytest.mark.unit
def test_properties_is_none():

    fields_class = fields(validators.ValidatorFieldInterface)

    assert fields_class[0].default is None
    assert fields_class[1].default is None
