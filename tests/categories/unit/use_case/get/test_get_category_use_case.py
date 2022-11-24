from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase

from kernel_catalogo_videos.core.domain.exceptions import NotFoundException

from kernel_catalogo_videos.categories.application.use_cases.get.input import (
    GetCategoryInput,
)
from kernel_catalogo_videos.categories.application.use_cases.get.output import (
    GetCategoryOutput,
)

from kernel_catalogo_videos.categories.application.use_cases.get.use_case import (
    GetCategoryUseCase,
)
from kernel_catalogo_videos.categories.infrastructure.repositories import (
    CategoryInMemoryRepository,
)
from kernel_catalogo_videos.categories.domain.entities import Category


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(GetCategoryUseCase, UseCase)


@pytest.mark.unit
def test_input():
    assert GetCategoryInput.__annotations__ == {"id": str}


@pytest.mark.unit
def test_execute():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=1,
    )
    # pylint: disable=unexpected-keyword-arg
    category = Category(**data)
    repo = CategoryInMemoryRepository()
    repo.items.append(category)

    with patch.object(repo, "find_by_id", wraps=repo.find_by_id) as mock_insert:

        input_params = GetCategoryInput(category.id)

        use_case = GetCategoryUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = GetCategoryOutput(
            id=category.id,
            title=category.title,
            description=category.description,
            status=category.status,
            is_deleted=category.is_deleted,
            created_at=category.created_at,
        )

    assert result == expected


@pytest.mark.unit
def test_raises_exception_when_category_not_found():
    repo = CategoryInMemoryRepository()
    input_params = GetCategoryInput("fake-id")
    use_case = GetCategoryUseCase(repo)
    with pytest.raises(NotFoundException) as assert_error:
        use_case.execute(input_params=input_params)

    assert assert_error.value.args[0] == "Entity not found using ID 'fake-id'"
