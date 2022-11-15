# Python
from abc import ABC
from dataclasses import dataclass, is_dataclass

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain import entities
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId


@dataclass(kw_only=True, frozen=True)
class StubEntity(entities.Entity):
    foo: str
    marco: str


@pytest.mark.unit
def test_entity_is_a_dataclass():
    assert is_dataclass(entities.Entity) is True


@pytest.mark.unit
def test_entity_is_a_abstract_class():
    assert isinstance(entities.Entity(), ABC)


@pytest.mark.unit
def test_entity_props():
    entity = StubEntity(foo="bar", marco="polo")
    assert entity.foo == "bar"
    assert entity.marco == "polo"
    assert isinstance(entity.unique_entity_id, UniqueEntityId)
    assert entity.unique_entity_id.id == entity.id

@pytest.mark.unit
def test_entity_set_valid_id():
    uuid = 'dcc13d20-e91d-437d-a6ac-2fd60605a271'
    entity = StubEntity(
        unique_entity_id=UniqueEntityId(uuid),
        foo="bar",
        marco="polo"
    )

    assert entity.id == uuid

@pytest.mark.unit
def test_entity_to_dict():
    uuid = 'dcc13d20-e91d-437d-a6ac-2fd60605a271'
    entity = StubEntity(
        unique_entity_id=UniqueEntityId(uuid),
        foo="bar",
        marco="polo"
    )

    assert entity.to_dict() == {"id": str(uuid), "foo": "bar", "marco": "polo"}