from datetime import datetime
from typing import Optional

import pytest

from kernel_catalogo_videos.castmembers.application.use_cases.dto import (
    CastMemberOutputDTO,
)
from kernel_catalogo_videos.castmembers.application.use_cases.get.output import (
    GetCastMemberOutput,
)


@pytest.mark.unit
def test_output():
    expected = {
        "id": str,
        "name": str,
        "kind": int,
        "is_deleted": bool,
        "created_at": datetime,
        "status": Optional[int],
    }

    assert CastMemberOutputDTO.__annotations__ == expected


@pytest.mark.unit
def test_get_castmember_output_is_subclass():
    assert issubclass(GetCastMemberOutput, CastMemberOutputDTO) is True
