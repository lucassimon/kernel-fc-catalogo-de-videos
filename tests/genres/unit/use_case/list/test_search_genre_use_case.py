from datetime import timedelta
from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.utils import now

from kernel_catalogo_videos.genres.application.use_cases.dto import (
    GenreOutputDTO,
    GenreOutputMapper,
)
from kernel_catalogo_videos.genres.application.use_cases.search.input import (
    SearchGenreInput,
)
from kernel_catalogo_videos.genres.application.use_cases.search.output import (
    SearchGenreOutput,
)

from kernel_catalogo_videos.genres.application.use_cases.search.use_case import (
    SearchGenresUseCase,
)
from kernel_catalogo_videos.genres.infrastructure.repositories import (
    GenreInMemoryRepository,
)
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(SearchGenresUseCase, UseCase)


@pytest.mark.unit
def test_execute_with_empty_search_params():
    # pylint: disable=unexpected-keyword-arg

    repo = GenreInMemoryRepository()
    repo.items = [
        Genre(title="test 1", created_at=now()),
        Genre(title="test 2", created_at=now() + timedelta(minutes=200)),
    ]
    with patch.object(repo, "search", wraps=repo.search) as mocked_search:
        input_params = SearchGenreInput()

        use_case = SearchGenresUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mocked_search.assert_called_once()

        items = list(
            map(
                lambda genre: GenreOutputMapper.to_output(
                    klass=GenreOutputDTO, genre=genre
                ),
                repo.items[::-1],
            )
        )

        expected = SearchGenreOutput(
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
        Genre(title="a"),
        Genre(title="AAA"),
        Genre(title="AaA"),
        Genre(title="b"),
        Genre(title="c"),
    ]

    repo = GenreInMemoryRepository()
    repo.items = items
    use_case = SearchGenresUseCase(repo)

    input_params = SearchGenreInput(
        page=1, per_page=2, sort="title", sort_direction="asc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda genre: GenreOutputMapper.to_output(
                klass=GenreOutputDTO, genre=genre
            ),
            [items[1], items[2]],
        )
    )

    expected = SearchGenreOutput(
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

    input_params = SearchGenreInput(
        page=2, per_page=2, sort="title", sort_direction="asc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda genre: GenreOutputMapper.to_output(
                klass=GenreOutputDTO, genre=genre
            ),
            [
                items[0],
            ],
        )
    )

    expected = SearchGenreOutput(
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

    input_params = SearchGenreInput(
        page=1, per_page=2, sort="title", sort_direction="desc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda genre: GenreOutputMapper.to_output(
                klass=GenreOutputDTO, genre=genre
            ),
            [items[0], items[2]],
        )
    )

    expected = SearchGenreOutput(
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

    input_params = SearchGenreInput(
        page=2, per_page=2, sort="title", sort_direction="desc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda genre: GenreOutputMapper.to_output(
                klass=GenreOutputDTO, genre=genre
            ),
            [
                items[1],
            ],
        )
    )

    expected = SearchGenreOutput(
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

    result = GenreRepository.SearchResult(items=[], **default_props)
    repo = GenreInMemoryRepository()
    use_case = SearchGenresUseCase(repo)
    output = use_case._SearchGenresUseCase__to_output( # pylint: disable=protected-access
        result=result
    )

    assert output == SearchGenreOutput(
        items=[],
        total=0,
        current_page=1,
        last_page=0,
        per_page=2,
        sort=None,
        sort_direction=None,
        filters=None,
    )


@pytest.mark.unit
def test_to_output_with_genre():
    entity = Genre(title="movie")
    default_props = {
        "total": 1,
        "current_page": 1,
        "per_page": 2,
        "sort": None,
        "sort_direction": None,
        "filters": None,
    }

    result = GenreRepository.SearchResult(items=[entity], **default_props)
    repo = GenreInMemoryRepository()
    use_case = SearchGenresUseCase(repo)
    output = use_case._SearchGenresUseCase__to_output( # pylint: disable=protected-access
        result=result
    )

    items = [GenreOutputMapper.to_output(klass=GenreOutputDTO, genre=entity)]
    assert output == PaginationOutputMapper.from_child(SearchGenreOutput).to_output(
        items, result
    )
