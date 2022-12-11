from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase

from kernel_catalogo_videos.core.domain.exceptions import NotFoundException

from kernel_catalogo_videos.genres.application.use_cases.delete.input import (
    DeleteGenreInput,
)

from kernel_catalogo_videos.genres.application.use_cases.delete.use_case import (
    DeleteGenreUseCase,
)
from kernel_catalogo_videos.genres.infrastructure.repositories import (
    GenreInMemoryRepository,
)
from kernel_catalogo_videos.genres.domain.entities import Genre


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(DeleteGenreUseCase, UseCase)


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

    with patch.object(repo, "delete", wraps=repo.delete) as mock_delete:

        input_params = DeleteGenreInput(genre.id)

        use_case = DeleteGenreUseCase(repo)
        use_case.execute(input_params=input_params)

        mock_delete.assert_called_once()

    assert repo.items == []


@pytest.mark.unit
def test_raises_exception_when_genre_not_found():
    repo = GenreInMemoryRepository()
    input_params = DeleteGenreInput("fake-id")
    use_case = DeleteGenreUseCase(repo)
    with pytest.raises(NotFoundException) as assert_error:
        use_case.execute(input_params=input_params)

    assert assert_error.value.args[0] == "Entity not found using ID 'fake-id'"
