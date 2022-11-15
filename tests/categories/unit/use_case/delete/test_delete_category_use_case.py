from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase

from kernel_catalogo_videos.core.domain.exceptions import NotFoundException

from kernel_catalogo_videos.categories.application.use_cases.delete.input import DeleteCategoryInput

from kernel_catalogo_videos.categories.application.use_cases.delete.use_case import DeleteCategoryUseCase
from kernel_catalogo_videos.categories.infrastructure.repositories import CategoryInMemoryRepository
from kernel_catalogo_videos.categories.domain.entities import Category


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(DeleteCategoryUseCase, UseCase)


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

    with patch.object(repo, "delete", wraps=repo.delete) as mock_delete:

        input_params = DeleteCategoryInput(category.id)

        use_case = DeleteCategoryUseCase(repo)
        use_case.execute(input_params=input_params)

        mock_delete.assert_called_once()

    assert repo.items == []


@pytest.mark.unit
def test_raises_exception_when_category_not_found():
    repo = CategoryInMemoryRepository()
    input_params = DeleteCategoryInput("fake-id")
    use_case = DeleteCategoryUseCase(repo)
    with pytest.raises(NotFoundException) as assert_error:
        use_case.execute(input_params=input_params)

    assert assert_error.value.args[0] == "Entity not found using ID 'fake-id'"
