# Python
import typing
from dataclasses import dataclass

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.entities import Entity
from kernel_catalogo_videos.core.domain.repositories import ET, Filter, SearchResult
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: int



@pytest.mark.unit
def test_props_annotations():
    assert SearchResult.__annotations__ == {
        'items': typing.List[ET],
        'current_page': int,
        'last_page': int,
        'per_page': int,
        'total': int,
        'filters': typing.Optional[Filter],
        'sort': typing.Optional[str],
        'sort_direction': typing.Optional[str],
    }

@pytest.mark.unit
def test_constructor_default_params():
    entity = StubEntity(name="some name", price=100)

    result = SearchResult(
        items=[entity, entity],
        total=4,
        current_page=1,
        per_page=2
    )

    assert result.to_dict() == {
        'items': [entity, entity],
        'total': 4,
        'current_page': 1,
        'per_page': 2,
        'last_page': 2,
        'sort': None,
        'sort_direction': None,
        'filters': None
    }



@pytest.mark.unit
def test_constructor_with_sort_and_filter_params():
    entity = StubEntity(name="some name", price=100)

    result = SearchResult(
        items=[entity, entity],
        total=4,
        current_page=1,
        per_page=2,
        sort='name',
        sort_direction='desc',
        filters='test'
    )

    assert result.to_dict() == {
        'items': [entity, entity],
        'total': 4,
        'current_page': 1,
        'per_page': 2,
        'last_page': 2,
        'sort': 'name',
        'sort_direction': 'desc',
        'filters': 'test'
    }


@pytest.mark.unit
def test_when_per_page_is_greater_than_total():
    result = SearchResult(
        items=[],
        total=4,
        current_page=1,
        per_page=15,
        sort='name',
        sort_direction='desc',
        filters='test'
    )

    assert result.last_page == 1


@pytest.mark.unit
def test_when_per_page_is_less_than_total():
    result = SearchResult(
        items=[],
        total=101,
        current_page=1,
        per_page=20,
        sort='name',
        sort_direction='desc',
        filters='test'
    )

    assert result.last_page == 6
