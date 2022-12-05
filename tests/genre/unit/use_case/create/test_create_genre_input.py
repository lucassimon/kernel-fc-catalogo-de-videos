from typing import Optional
import pytest

from kernel_catalogo_videos.genres.application.use_cases.create.input import (
    CreateGenreInput,
)
from kernel_catalogo_videos.genres.domain.entities import Genre


@pytest.mark.unit
def test_input():
    expected = {"title": str,  "status": Optional[int]}

    assert CreateGenreInput.__annotations__ == expected


@pytest.mark.unit
def test_status_field():
    # pylint: disable=no-member
    status_field = CreateGenreInput.__dataclass_fields__["status"]

    assert status_field.default == Genre.get_field("status").default
