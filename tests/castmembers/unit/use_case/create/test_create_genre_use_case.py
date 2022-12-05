from unittest.mock import patch
from typing import Optional
import pytest

from kernel_catalogo_videos.castmembers.application.use_cases.create.input import (
    CreateCastMemberInput,
)
from kernel_catalogo_videos.castmembers.application.use_cases.create.output import (
    CreateCastMemberOutput,
)

from kernel_catalogo_videos.castmembers.application.use_cases.create.use_case import (
    CreateGenreUseCase,
)
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.castmembers.infrastructure.repositories import (
    CastMemberInMemoryRepository,
)


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(CreateGenreUseCase, UseCase)



@pytest.mark.unit
def test_execute():
    repo = CastMemberInMemoryRepository()
    with patch.object(repo, "insert", wraps=repo.insert) as mock_insert:
        input_params = CreateCastMemberInput(
            name="some title", kind=1, status=1
        )
        use_case = CreateGenreUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mock_insert.assert_called_once()

        expected = CreateCastMemberOutput(
            id=repo.items[0].id,
            name="some title",
            kind=1,
            status=1,
            is_deleted=False,
            created_at=repo.items[0].created_at,
        )

    assert result == expected
