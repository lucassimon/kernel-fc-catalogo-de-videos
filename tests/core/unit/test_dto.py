import pytest

from typing import List, Optional
from kernel_catalogo_videos.core.application.dto import (
    Item,
    PaginationOutput,
    PaginationOutputMapper,
    SearchInput,
    Filter,
)
from kernel_catalogo_videos.core.domain.repositories import SearchResult


class StubPaginationOutputChild(PaginationOutput):
    pass


@pytest.mark.unit
def test_search_input():
    expected = {
        "page": Optional[int],
        "per_page": Optional[int],
        "sort": Optional[str],
        "sort_direction": Optional[str],
        "filters": Optional[Filter],
    }

    assert SearchInput.__annotations__ == expected


@pytest.mark.unit
def test_pagination_output():
    expected = {
        "items": List[Item],
        "current_page": int,
        "per_page": int,
        "last_page": int,
        "sort": Optional[str],
        "sort_direction": Optional[str],
        "filters": Optional[Filter],
        "total": int,
    }

    assert PaginationOutput.__annotations__ == expected


@pytest.mark.unit
def test_pagination_output_mapper_from_child():
    mapper = PaginationOutputMapper.from_child(StubPaginationOutputChild)

    assert isinstance(mapper, PaginationOutputMapper)
    assert issubclass(mapper.output_child, StubPaginationOutputChild)


@pytest.mark.unit
def test_pagination_output_mapper_to_output():
    result = SearchResult(
        items=["some-item"],
        total=1,
        current_page=1,
        per_page=1,
        sort="name",
        sort_direction="asc",
        filters="filter fake",
    )

    output = PaginationOutputMapper.from_child(StubPaginationOutputChild).to_output(
        result=result, items=result.items
    )

    expected = StubPaginationOutputChild(
        items=["some-item"],
        total=1,
        current_page=1,
        per_page=1,
        sort="name",
        sort_direction="asc",
        filters="filter fake",
        last_page=1,
    )

    assert output == expected
