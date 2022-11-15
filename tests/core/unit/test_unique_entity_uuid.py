# Python
import uuid
from dataclasses import FrozenInstanceError, is_dataclass
from unittest.mock import patch

# Third
import pytest

# Apps
from kernel_catalogo_videos.core import utils
from kernel_catalogo_videos.core.domain import exceptions
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId


@pytest.mark.unit
def test_unique_entity_uuid_is_a_dataclass():
    assert is_dataclass(UniqueEntityId) is True

@pytest.mark.unit
def test_raises_an_exception_when_uuid_is_invalid():
    with patch.object(
        UniqueEntityId,
        '_UniqueEntityId__validate',
        autospec=True,
        side_effect=UniqueEntityId._UniqueEntityId__validate
    ) as mock_validate:
        with pytest.raises(exceptions.InvalidUUIDException) as assert_error:
            UniqueEntityId('invalid id')

        mock_validate.assert_called_once()

        assert assert_error.value.args[0] == 'Id must be a valid UUID'


@pytest.mark.unit
def test_valid_uuid_as_string():
    with patch.object(
        UniqueEntityId,
        '_UniqueEntityId__validate',
        autospec=True,
        side_effect=UniqueEntityId._UniqueEntityId__validate
    ) as mock_validate:
        uuid = 'dcc13d20-e91d-437d-a6ac-2fd60605a271'
        obj = UniqueEntityId(uuid)
        mock_validate.assert_called_once()
        assert obj.id == str(uuid)

@pytest.mark.unit
def test_valid_uuid_as_uuid_generated():
    with patch.object(
        UniqueEntityId,
        '_UniqueEntityId__validate',
        autospec=True,
        side_effect=UniqueEntityId._UniqueEntityId__validate
    ) as mock_validate:
        uuid = utils.uuidv4()
        obj = UniqueEntityId(uuid)
        mock_validate.assert_called_once()
        assert obj.id == str(uuid)


@pytest.mark.unit
def test_uuid_generated_when_default_params():
    with patch.object(
        UniqueEntityId,
        '_UniqueEntityId__validate',
        autospec=True,
        side_effect=UniqueEntityId._UniqueEntityId__validate
    ) as mock_validate:
        obj = UniqueEntityId()
        uuid.UUID(obj.id)
        mock_validate.assert_called_once()


@pytest.mark.unit
def test_is_immutable():
    obj = UniqueEntityId()
    with pytest.raises(FrozenInstanceError):
        obj.id = 'set another id'

@pytest.mark.unit
def test_dunder_str():
    uuid = utils.uuidv4()
    obj = UniqueEntityId(uuid)

    assert obj.__str__() == str(uuid)
