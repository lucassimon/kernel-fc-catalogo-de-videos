# Python
from typing import List, Optional
from dataclasses import dataclass

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.entities import Entity
from kernel_catalogo_videos.core.domain.repositories import Filter, SearchParams, InMemorySearchableRepository, SearchResult


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: int


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ["name", "price"]

    def _apply_filter(self, items: List[StubEntity], filters: Optional[Filter]):
        if filters:
            items_filtered = filter(
                lambda item: filters.lower() in item.name.lower() or filters == str(item.price), items
            )
            return list(items_filtered)

        return items


def make_repo():
    return StubInMemorySearchableRepository()


# pylint: disable=unexpected-keyword-arg


@pytest.mark.unit
@pytest.mark.parametrize(
    "items, param, expected",
    [
        (
            [StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="test", price=100)],
            None,
            [StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="test", price=100)],
        ),
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="test", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="TEST", price=300),
                StubEntity(name="fake", price=500),
            ],
            "TEST",
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="test", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="TEST", price=300),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="test", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="TEST", price=300),
                StubEntity(name="fake", price=500),
            ],
            "300",
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="TEST", price=300),
            ],
        ),
    ],
)
def test_apply_filter(items, param, expected):
    repo = make_repo()
    # pylint: disable=protected-access
    result = repo._apply_filter(items, param)

    assert result == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "items, field_name, direction, expected",
    [
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
            ],
            "name",
            "asc",
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
            "price",
            "asc",
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
            "name",
            "desc",
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
            "price",
            "desc",
            [
                StubEntity(unique_entity_id="7e8453bc-25f8-454a-9d79-d94d5acc32b7", name="a", price=300),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
        ),
    ],
)
def test_apply_sort(items, field_name, direction, expected):
    repo = make_repo()
    # pylint: disable=protected-access
    result = repo._apply_sort(items, sort=field_name, sort_direction=direction)

    assert result == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "items, page, per_page, expected",
    [
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="a", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="c", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="d", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="e", price=100),
            ],
            1,
            2,
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="a", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="a", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="c", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="d", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="e", price=100),
            ],
            2,
            2,
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="c", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="d", price=100),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="a", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="c", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="d", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="e", price=100),
            ],
            3,
            2,
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="e", price=100),
            ],
        ),
        (
            [
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="a", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="b", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="c", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="d", price=100),
                StubEntity(unique_entity_id="dcc13d20-e91d-437d-a6ac-2fd60605a271", name="e", price=100),
            ],
            4,
            2,
            [],
        ),
    ],
)
def test_apply_paginate(items, page, per_page, expected):
    repo = make_repo()
    # pylint: disable=protected-access
    result = repo._apply_paginate(items, page=page, per_page=per_page)

    assert result == expected


@pytest.mark.unit
def test_search_when_params_is_empty():
    entity = StubEntity(name="a", price=100)
    items = [entity] * 2
    repo = make_repo()
    repo.items = items

    result = repo.search(SearchParams())
    assert result == SearchResult(
        items=[entity] * 2,
        total=2,
        current_page=1,
        per_page=10,
        sort=None,
        sort_direction="asc",
        filters=None,
    )


@pytest.mark.unit
def test_search_applying_filter_and_paginate():
    items = [
        StubEntity(name="test", price=100),
        StubEntity(name="a", price=100),
        StubEntity(name="TEST", price=100),
        StubEntity(name="TeSt", price=100),
    ]
    repo = make_repo()
    repo.items = items

    result = repo.search(SearchParams(page=1, per_page=2, filters="TEST"))

    assert result == SearchResult(
        items=[items[0], items[2]],
        total=3,
        current_page=1,
        per_page=2,
        sort=None,
        sort_direction="asc",
        filters="TEST",
    )

    result = repo.search(SearchParams(page=2, per_page=2, filters="TEST"))

    assert result == SearchResult(
        items=[items[3]],
        total=3,
        current_page=2,
        per_page=2,
        sort=None,
        sort_direction="asc",
        filters="TEST",
    )

    result = repo.search(SearchParams(page=3, per_page=2, filters="TEST"))

    assert result == SearchResult(
        items=[],
        total=3,
        current_page=3,
        per_page=2,
        sort=None,
        sort_direction="asc",
        filters="TEST",
    )


@pytest.mark.unit
def test_search_applying_sort_and_paginate():
    items = [
        StubEntity(name="b", price=100),
        StubEntity(name="a", price=100),
        StubEntity(name="d", price=100),
        StubEntity(name="e", price=100),
        StubEntity(name="c", price=100),
    ]
    repo = make_repo()
    repo.items = items

    result = repo.search(SearchParams(page=1, per_page=2, sort="name"))

    assert result == SearchResult(
        items=[items[1], items[0]],
        total=5,
        current_page=1,
        per_page=2,
        sort="name",
        sort_direction="asc",
        filters=None,
    )

    result = repo.search(SearchParams(page=2, per_page=2, sort="name"))

    assert result == SearchResult(
        items=[items[4], items[2]],
        total=5,
        current_page=2,
        per_page=2,
        sort="name",
        sort_direction="asc",
        filters=None,
    )

    result = repo.search(SearchParams(page=3, per_page=2, sort="name"))

    assert result == SearchResult(
        items=[items[3]],
        total=5,
        current_page=3,
        per_page=2,
        sort="name",
        sort_direction="asc",
        filters=None,
    )


@pytest.mark.unit
def test_search_applying_filter_sort_and_paginate():
    items = [
        StubEntity(name="test", price=100),
        StubEntity(name="a", price=100),
        StubEntity(name="TEST", price=100),
        StubEntity(name="e", price=100),
        StubEntity(name="TeSt", price=100),
    ]
    repo = make_repo()
    repo.items = items

    result = repo.search(SearchParams(page=1, per_page=2, sort="name", filters="TEST"))

    assert result == SearchResult(
        items=[items[2], items[4]],
        total=3,
        current_page=1,
        per_page=2,
        sort="name",
        sort_direction="asc",
        filters="TEST",
    )

    result = repo.search(SearchParams(page=2, per_page=2, sort="name", filters="TEST"))

    assert result == SearchResult(
        items=[items[0]],
        total=3,
        current_page=2,
        per_page=2,
        sort="name",
        sort_direction="asc",
        filters="TEST",
    )
