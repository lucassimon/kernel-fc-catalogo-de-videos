# Python
from abc import ABC
from dataclasses import is_dataclass
from datetime import datetime, timezone
from unittest import mock

# Third
import pytest

# Apps
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId

utc = timezone.utc


@pytest.mark.unit
def test_create_entity_successfully():
    castmember = CastMember(name="foo", kind=1)

    assert castmember.name == "foo"
    assert castmember.kind == 1


@pytest.mark.unit
def test_entity_is_a_dataclass():
    assert is_dataclass(CastMember) is True


@pytest.mark.unit
def test_entity_is_a_abstract_class():
    assert isinstance(CastMember(name="Foo", kind=1), ABC)


@pytest.mark.unit
def test_entity_props():
    entity = CastMember(name="bar", kind=1)
    assert isinstance(entity.unique_entity_id, UniqueEntityId)
    assert entity.unique_entity_id.id == entity.id


@pytest.mark.unit
def test_entity_set_valid_id():
    uuid = "dcc13d20-e91d-437d-a6ac-2fd60605a271"
    entity = CastMember(unique_entity_id=UniqueEntityId(uuid), name="bar", kind=1)

    assert entity.id == uuid


@pytest.mark.unit
def test_entity_to_dict():
    uuid = "dcc13d20-e91d-437d-a6ac-2fd60605a271"
    entity = CastMember(
        unique_entity_id=UniqueEntityId(uuid),
        name="bar",
        kind=1,
        created_at=datetime(2019, 7, 1),
    )

    assert entity.to_dict() == {
        "id": str(uuid),
        "name": "bar",
        "kind": 1,
        "status": 1,
        "is_deleted": False,
        "created_at": datetime(2019, 7, 1),
    }
