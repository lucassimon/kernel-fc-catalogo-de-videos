import pytest

from kernel_catalogo_videos.castmembers.application.use_cases.delete.input import (
    DeleteCastMemberInput,
)


@pytest.mark.unit
def test_input():
    expected = {"id": str}

    assert DeleteCastMemberInput.__annotations__ == expected
