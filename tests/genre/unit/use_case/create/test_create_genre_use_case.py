from unittest.mock import patch
from typing import Optional
import pytest

from kernel_catalogo_videos.genres.application.use_cases.create.input import (
    CreateGenreInput,
)
from kernel_catalogo_videos.genres.application.use_cases.create.output import (
    CreateGenreOutput,
)

from kernel_catalogo_videos.genres.application.use_cases.create.use_case import (
    CreateGenreUseCase,
)
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.infrastructure.repositories import (
    GenreInMemoryRepository,
)


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(CreateGenreUseCase, UseCase)



@pytest.mark.unit
def test_execute():
    repo = GenreInMemoryRepository()
    with patch.object(repo, "insert", wraps=repo.insert) as mock_insert:
        input_params = CreateGenreInput(
            title="some title", status=1
        )
        use_case = CreateGenreUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = CreateGenreOutput(
            id=repo.items[0].id,
            title="some title",
            slug="some-title",
            status=1,
            is_deleted=False,
            created_at=repo.items[0].created_at,
        )

    assert result == expected
