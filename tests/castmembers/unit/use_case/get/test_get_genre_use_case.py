from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase

from kernel_catalogo_videos.core.domain.exceptions import NotFoundException

from kernel_catalogo_videos.castmembers.application.use_cases.get.input import (
    GetCastMemberInput,
)
from kernel_catalogo_videos.castmembers.application.use_cases.get.output import (
    GetCastMemberOutput,
)

from kernel_catalogo_videos.castmembers.application.use_cases.get.use_case import (
    GetCastMemberUseCase,
)
from kernel_catalogo_videos.castmembers.infrastructure.repositories import (
    CastMemberInMemoryRepository,
)
from kernel_catalogo_videos.castmembers.domain.entities import CastMember


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(GetCastMemberUseCase, UseCase)


@pytest.mark.unit
def test_input():
    assert GetCastMemberInput.__annotations__ == {"id": str}


@pytest.mark.unit
def test_execute():
    data = dict(
        name="some test",
        kind=1,
        status=1,
    )
    # pylint: disable=unexpected-keyword-arg
    castmember = CastMember(**data)
    repo = CastMemberInMemoryRepository()
    repo.items.append(castmember)

    with patch.object(repo, "find_by_id", wraps=repo.find_by_id) as mock_insert:

        input_params = GetCastMemberInput(castmember.id)

        use_case = GetCastMemberUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = GetCastMemberOutput(
            id=castmember.id,
            name=castmember.name,
            kind=castmember.kind,
            status=castmember.status,
            is_deleted=castmember.is_deleted,
            created_at=castmember.created_at,
        )

    assert result == expected


@pytest.mark.unit
def test_raises_exception_when_genre_not_found():
    repo = CastMemberInMemoryRepository()
    input_params = GetCastMemberInput("fake-id")
    use_case = GetCastMemberUseCase(repo)
    with pytest.raises(NotFoundException) as assert_error:
        use_case.execute(input_params=input_params)

    assert assert_error.value.args[0] == "Entity not found using ID 'fake-id'"
