import pytest

from kernel_catalogo_videos.genres.application.use_cases.delete.input import (
    DeleteGenreInput,
)


@pytest.mark.unit
def test_input():
    expected = {"id": str}

    assert DeleteGenreInput.__annotations__ == expected
