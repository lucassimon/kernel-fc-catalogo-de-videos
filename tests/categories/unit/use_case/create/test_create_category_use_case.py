from unittest.mock import patch
from typing import Optional
import pytest

from kernel_catalogo_videos.categories.application.use_cases.create.input import (
    CreateCategoryInput,
)
from kernel_catalogo_videos.categories.application.use_cases.create.output import (
    CreateCategoryOutput,
)

from kernel_catalogo_videos.categories.application.use_cases.create.use_case import (
    CreateCategoryUseCase,
)
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.infrastructure.repositories import (
    CategoryInMemoryRepository,
)


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(CreateCategoryUseCase, UseCase)


@pytest.mark.unit
def test_input():
    assert CreateCategoryInput.__annotations__ == {
        "title": str,
        "description": Optional[str],
        "status": Optional[int],
    }


@pytest.mark.unit
def test_execute():
    repo = CategoryInMemoryRepository()
    with patch.object(repo, "insert", wraps=repo.insert) as mock_insert:
        input_params = CreateCategoryInput(
            title="some title", description="some description", status=1
        )
        use_case = CreateCategoryUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = CreateCategoryOutput(
            id=repo.items[0].id,
            title="some title",
            slug="some-title",
            description="some description",
            status=1,
            is_deleted=False,
            created_at=repo.items[0].created_at,
        )

    assert result == expected
