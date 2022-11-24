from typing import Optional
import pytest

from kernel_catalogo_videos.categories.application.use_cases.create.input import (
    CreateCategoryInput,
)
from kernel_catalogo_videos.categories.domain.entities import Category


@pytest.mark.unit
def test_input():
    expected = {"title": str, "description": Optional[str], "status": Optional[int]}

    assert CreateCategoryInput.__annotations__ == expected


@pytest.mark.unit
def test_description_field():
    # pylint: disable=no-member
    description_field = CreateCategoryInput.__dataclass_fields__["description"]

    assert description_field.default == Category.get_field("description").default


@pytest.mark.unit
def test_status_field():
    # pylint: disable=no-member
    status_field = CreateCategoryInput.__dataclass_fields__["status"]

    assert status_field.default == Category.get_field("status").default
