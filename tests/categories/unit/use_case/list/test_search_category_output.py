from typing import List, Optional


import pytest

from kernel_catalogo_videos.categories.application.use_cases.search.output import SearchCategoryOutput
from kernel_catalogo_videos.core.application.dto import Filter, Item, PaginationOutput


@pytest.mark.unit
@pytest.mark.skip
def test_output():
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
    assert SearchCategoryOutput.__annotations__ == expected


@pytest.mark.unit
def test_output_is_search_input():
    assert issubclass(SearchCategoryOutput, PaginationOutput)
