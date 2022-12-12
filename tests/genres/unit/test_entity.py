# Python
from abc import ABC
from dataclasses import is_dataclass
from datetime import datetime, timezone
from unittest import mock

# Third
import pytest

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId

utc = timezone.utc


@pytest.mark.unit
def test_create_entity_successfully():
    genre = Genre(title="foo", slug="foo", categories=["some-uuid"],)

    assert genre.title == "foo"
    assert genre.slug == "foo"
    assert genre.categories == ["some-uuid"]


@pytest.mark.unit
def test_entity_is_a_dataclass():
    assert is_dataclass(Genre) is True


@pytest.mark.unit
def test_entity_is_a_abstract_class():
    assert isinstance(Genre(title="Foo", slug="Bar", categories=["some-uuid"],), ABC)


@pytest.mark.unit
def test_entity_props():
    entity = Genre(title="bar", slug="polo", categories=["some-uuid"],)
    assert isinstance(entity.unique_entity_id, UniqueEntityId)
    assert entity.unique_entity_id.id == entity.id


@pytest.mark.unit
def test_entity_set_valid_id():
    uuid = "dcc13d20-e91d-437d-a6ac-2fd60605a271"
    entity = Genre(unique_entity_id=UniqueEntityId(uuid), title="bar", slug="polo", categories=["some-uuid"],)

    assert entity.id == uuid


@pytest.mark.unit
def test_entity_to_dict():
    uuid = "dcc13d20-e91d-437d-a6ac-2fd60605a271"
    entity = Genre(
        unique_entity_id=UniqueEntityId(uuid),
        title="bar",
        categories=["some-uuid"],
        created_at=datetime(2019, 7, 1),
    )

    assert entity.to_dict() == {
        "id": str(uuid),
        "title": "bar",
        "slug": "bar",
        "categories": ["some-uuid"],
        "status": 1,
        "is_deleted": False,
        "created_at": datetime(2019, 7, 1),
    }
