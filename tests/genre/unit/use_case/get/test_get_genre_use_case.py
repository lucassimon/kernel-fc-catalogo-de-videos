from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase

from kernel_catalogo_videos.core.domain.exceptions import NotFoundException

from kernel_catalogo_videos.genres.application.use_cases.get.input import (
    GetGenreInput,
)
from kernel_catalogo_videos.genres.application.use_cases.get.output import (
    GetGenreOutput,
)

from kernel_catalogo_videos.genres.application.use_cases.get.use_case import (
    GetGenreUseCase,
)
from kernel_catalogo_videos.genres.infrastructure.repositories import (
    GenreInMemoryRepository,
)
from kernel_catalogo_videos.genres.domain.entities import Genre


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(GetGenreUseCase, UseCase)


@pytest.mark.unit
def test_input():
    assert GetGenreInput.__annotations__ == {"id": str}


@pytest.mark.unit
def test_execute():
    data = dict(
        title="some test",
        slug="some-test",
        status=1,
    )
    # pylint: disable=unexpected-keyword-arg
    genre = Genre(**data)
    repo = GenreInMemoryRepository()
    repo.items.append(genre)

    with patch.object(repo, "find_by_id", wraps=repo.find_by_id) as mock_insert:

        input_params = GetGenreInput(genre.id)

        use_case = GetGenreUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = GetGenreOutput(
            id=genre.id,
            title=genre.title,
            slug=genre.slug,
            status=genre.status,
            is_deleted=genre.is_deleted,
            created_at=genre.created_at,
        )

    assert result == expected


@pytest.mark.unit
def test_raises_exception_when_genre_not_found():
    repo = GenreInMemoryRepository()
    input_params = GetGenreInput("fake-id")
    use_case = GetGenreUseCase(repo)
    with pytest.raises(NotFoundException) as assert_error:
        use_case.execute(input_params=input_params)

    assert assert_error.value.args[0] == "Entity not found using ID 'fake-id'"
