import pytest

from kernel_catalogo_videos.categories.application.use_cases.delete.input import DeleteCategoryInput


@pytest.mark.unit
def test_input():
    expected = {"id": str}

    assert DeleteCategoryInput.__annotations__ == expected
