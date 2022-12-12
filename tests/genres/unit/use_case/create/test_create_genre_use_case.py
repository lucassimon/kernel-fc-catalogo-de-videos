from unittest.mock import patch
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
from kernel_catalogo_videos.categories.infrastructure.repositories import (
    CategoryInMemoryRepository
)
from kernel_catalogo_videos.categories.domain.services import CategoryService


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(CreateGenreUseCase, UseCase)



@pytest.mark.unit
def test_execute():
    repo = GenreInMemoryRepository()
    category_repo = CategoryInMemoryRepository()
    category_service = CategoryService(repo=category_repo)
    with patch.object(repo, "insert", wraps=repo.insert) as mock_insert:
        input_params = CreateGenreInput(
            title="some title", status=1, categories=["some uuid"]
        )
        use_case = CreateGenreUseCase(repo=repo, category_service=category_service)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = CreateGenreOutput(
            id=repo.items[0].id,
            title="some title",
            slug="some-title",
            categories=["some uuid"],
            status=1,
            is_deleted=False,
            created_at=repo.items[0].created_at,
        )

    assert result == expected
