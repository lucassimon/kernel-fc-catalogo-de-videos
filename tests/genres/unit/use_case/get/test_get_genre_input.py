import pytest

from kernel_catalogo_videos.genres.application.use_cases.get.input import (
    GetGenreInput,
)


@pytest.mark.unit
def test_input():
    expected = {"id": str}

    assert GetGenreInput.__annotations__ == expected
