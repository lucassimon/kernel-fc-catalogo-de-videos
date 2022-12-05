import pytest

from kernel_catalogo_videos.castmembers.application.use_cases.get.input import (
    GetCastMemberInput,
)


@pytest.mark.unit
def test_input():
    expected = {"id": str}

    assert GetCastMemberInput.__annotations__ == expected
