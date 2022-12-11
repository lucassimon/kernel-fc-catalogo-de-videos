from datetime import datetime
from typing import Optional

import pytest

from kernel_catalogo_videos.genres.application.use_cases.dto import (
    GenreOutputDTO,
)
from kernel_catalogo_videos.genres.application.use_cases.get.output import (
    GetGenreOutput,
)


@pytest.mark.unit
def test_output():
    expected = {
        "id": str,
        "title": str,
        "slug": str,
        "is_deleted": bool,
        "created_at": datetime,
        "status": Optional[int],
    }

    assert GenreOutputDTO.__annotations__ == expected


@pytest.mark.unit
def test_get_genre_output_is_subclass():
    assert issubclass(GetGenreOutput, GenreOutputDTO) is True
