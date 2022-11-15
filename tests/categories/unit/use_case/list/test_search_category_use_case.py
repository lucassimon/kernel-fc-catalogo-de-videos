from datetime import timedelta
from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.utils import now

from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputDTO, CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.search.input import SearchCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.search.output import SearchCategoryOutput

from kernel_catalogo_videos.categories.application.use_cases.search.use_case import SearchCategoriesUseCase
from kernel_catalogo_videos.categories.infrastructure.repositories import CategoryInMemoryRepository
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(SearchCategoriesUseCase, UseCase)


@pytest.mark.unit
def test_execute_with_empty_search_params():
    # pylint: disable=unexpected-keyword-arg

    repo = CategoryInMemoryRepository()
    repo.items = [
        Category(title="test 1", created_at=now()),
        Category(title="test 2", created_at=now() + timedelta(minutes=200)),
    ]
    with patch.object(repo, "search", wraps=repo.search) as mocked_search:
        input_params = SearchCategoryInput()

        use_case = SearchCategoriesUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mocked_search.assert_called_once()

        items = list(
            map(
                lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
                repo.items[::-1],
            )
        )

        expected = SearchCategoryOutput(
            items=items,
            current_page=1,
            per_page=10,
            last_page=1,
            total=2,
            sort=None,
            sort_direction="asc",
            filters=None,
        )

    assert result == expected


@pytest.mark.unit
def test_execute_with_pagination_and_sort_filter():
    # pylint: disable=unexpected-keyword-arg

    items = [
        Category(title="a"),
        Category(title="AAA"),
        Category(title="AaA"),
        Category(title="b"),
        Category(title="c"),
    ]

    repo = CategoryInMemoryRepository()
    repo.items = items
    use_case = SearchCategoriesUseCase(repo)

    input_params = SearchCategoryInput(page=1, per_page=2, sort="title", sort_direction="asc", filters="a")

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
            [items[1], items[2]],
        )
    )

    expected = SearchCategoryOutput(
        items=items_expected,
        current_page=1,
        per_page=2,
        last_page=2,
        total=3,
        sort="title",
        sort_direction="asc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCategoryInput(page=2, per_page=2, sort="title", sort_direction="asc", filters="a")

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
            [
                items[0],
            ],
        )
    )

    expected = SearchCategoryOutput(
        items=items_expected,
        current_page=2,
        per_page=2,
        last_page=2,
        total=3,
        sort="title",
        sort_direction="asc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCategoryInput(page=1, per_page=2, sort="title", sort_direction="desc", filters="a")

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
            [items[0], items[2]],
        )
    )

    expected = SearchCategoryOutput(
        items=items_expected,
        current_page=1,
        per_page=2,
        last_page=2,
        total=3,
        sort="title",
        sort_direction="desc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCategoryInput(page=2, per_page=2, sort="title", sort_direction="desc", filters="a")

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda category: CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=category),
            [
                items[1],
            ],
        )
    )

    expected = SearchCategoryOutput(
        items=items_expected,
        current_page=2,
        per_page=2,
        last_page=2,
        total=3,
        sort="title",
        sort_direction="desc",
        filters="a",
    )

    assert result == expected


@pytest.mark.unit
def test_to_output_when_empty_response():

    default_props = {
        "total": 0,
        "current_page": 1,
        "per_page": 2,
        "sort": None,
        "sort_direction": None,
        "filters": None,
    }

    result = CategoryRepository.SearchResult(items=[], **default_props)
    repo = CategoryInMemoryRepository()
    use_case = SearchCategoriesUseCase(repo)
    output = use_case._SearchCategoriesUseCase__to_output(result=result)  # pylint: disable=protected-access

    assert output == SearchCategoryOutput(
        items=[], total=0, current_page=1, last_page=0, per_page=2, sort=None, sort_direction=None, filters=None
    )


@pytest.mark.unit
def test_to_output_with_category():
    entity = Category(title="movie")
    default_props = {
        "total": 1,
        "current_page": 1,
        "per_page": 2,
        "sort": None,
        "sort_direction": None,
        "filters": None,
    }

    result = CategoryRepository.SearchResult(items=[entity], **default_props)
    repo = CategoryInMemoryRepository()
    use_case = SearchCategoriesUseCase(repo)
    output = use_case._SearchCategoriesUseCase__to_output(result=result)  # pylint: disable=protected-access

    items = [CategoryOutputMapper.to_output(klass=CategoryOutputDTO, category=entity)]
    assert output == PaginationOutputMapper.from_child(SearchCategoryOutput).to_output(items, result)
