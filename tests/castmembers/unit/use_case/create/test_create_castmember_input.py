from typing import Optional
import pytest

from kernel_catalogo_videos.castmembers.application.use_cases.create.input import (
    CreateCastMemberInput,
)
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


@pytest.mark.unit
def test_input():
    expected = {"name": str, "kind": int,  "status": Optional[int]}

    assert CreateCastMemberInput.__annotations__ == expected


@pytest.mark.unit
def test_status_field():
    # pylint: disable=no-member
    status_field = CreateCastMemberInput.__dataclass_fields__["status"]

    assert status_field.default == CastMember.get_field("status").default
