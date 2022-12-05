from datetime import timedelta
from unittest.mock import patch
import pytest
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.core.application.dto import PaginationOutputMapper
from kernel_catalogo_videos.core.utils import now

from kernel_catalogo_videos.castmembers.application.use_cases.dto import (
    CastMemberOutputDTO,
    CastMemberOutputMapper,
)
from kernel_catalogo_videos.castmembers.application.use_cases.search.input import (
    SearchCastMemberInput,
)
from kernel_catalogo_videos.castmembers.application.use_cases.search.output import (
    SearchCastMemberOutput,
)

from kernel_catalogo_videos.castmembers.application.use_cases.search.use_case import (
    SearchCastMembersUseCase,
)
from kernel_catalogo_videos.castmembers.infrastructure.repositories import (
    CastMemberInMemoryRepository,
)
from kernel_catalogo_videos.castmembers.domain.entities import CastMember
from kernel_catalogo_videos.castmembers.domain.repositories import CastMemberRepository


@pytest.mark.unit
def test_is_subclass():
    assert issubclass(SearchCastMembersUseCase, UseCase)


@pytest.mark.unit
def test_execute_with_empty_search_params():
    # pylint: disable=unexpected-keyword-arg

    repo = CastMemberInMemoryRepository()
    repo.items = [
        CastMember(name="test 1", kind=1, created_at=now()),
        CastMember(name="test 2", kind=1, created_at=now() + timedelta(minutes=200)),
    ]
    with patch.object(repo, "search", wraps=repo.search) as mocked_search:
        input_params = SearchCastMemberInput()

        use_case = SearchCastMembersUseCase(repo)
        result = use_case.execute(input_params=input_params)

        mocked_search.assert_called_once()

        items = list(
            map(
                lambda castmember: CastMemberOutputMapper.to_output(
                    klass=CastMemberOutputDTO, castmember=castmember
                ),
                repo.items[::-1],
            )
        )

        expected = SearchCastMemberOutput(
            items=items,
            current_page=1,
            per_page=10,
            last_page=1,
            total=2,
            sort=None,
            sort_direction="asc",
            filters=None,
        )

    assert result == expected


@pytest.mark.unit
def test_execute_with_pagination_and_sort_filter():
    # pylint: disable=unexpected-keyword-arg

    items = [
        CastMember(name="a", kind=1),
        CastMember(name="AAA", kind=1),
        CastMember(name="AaA", kind=1),
        CastMember(name="b", kind=1),
        CastMember(name="c", kind=1),
    ]

    repo = CastMemberInMemoryRepository()
    repo.items = items
    use_case = SearchCastMembersUseCase(repo)

    input_params = SearchCastMemberInput(
        page=1, per_page=2, sort="name", sort_direction="asc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda castmember: CastMemberOutputMapper.to_output(
                klass=CastMemberOutputDTO, castmember=castmember
            ),
            [items[1], items[2]],
        )
    )

    expected = SearchCastMemberOutput(
        items=items_expected,
        current_page=1,
        per_page=2,
        last_page=2,
        total=3,
        sort="name",
        sort_direction="asc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCastMemberInput(
        page=2, per_page=2, sort="name", sort_direction="asc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda castmember: CastMemberOutputMapper.to_output(
                klass=CastMemberOutputDTO, castmember=castmember
            ),
            [
                items[0],
            ],
        )
    )

    expected = SearchCastMemberOutput(
        items=items_expected,
        current_page=2,
        per_page=2,
        last_page=2,
        total=3,
        sort="name",
        sort_direction="asc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCastMemberInput(
        page=1, per_page=2, sort="name", sort_direction="desc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda castmember: CastMemberOutputMapper.to_output(
                klass=CastMemberOutputDTO, castmember=castmember
            ),
            [items[0], items[2]],
        )
    )

    expected = SearchCastMemberOutput(
        items=items_expected,
        current_page=1,
        per_page=2,
        last_page=2,
        total=3,
        sort="name",
        sort_direction="desc",
        filters="a",
    )

    assert result == expected

    input_params = SearchCastMemberInput(
        page=2, per_page=2, sort="name", sort_direction="desc", filters="a"
    )

    result = use_case.execute(input_params=input_params)

    items_expected = list(
        map(
            lambda castmember: CastMemberOutputMapper.to_output(
                klass=CastMemberOutputDTO, castmember=castmember
            ),
            [
                items[1],
            ],
        )
    )

    expected = SearchCastMemberOutput(
        items=items_expected,
        current_page=2,
        per_page=2,
        last_page=2,
        total=3,
        sort="name",
        sort_direction="desc",
        filters="a",
    )

    assert result == expected


@pytest.mark.unit
def test_to_output_when_empty_response():

    default_props = {
        "total": 0,
        "current_page": 1,
        "per_page": 2,
        "sort": None,
        "sort_direction": None,
        "filters": None,
    }

    result = CastMemberRepository.SearchResult(items=[], **default_props)
    repo = CastMemberInMemoryRepository()
    use_case = SearchCastMembersUseCase(repo)
    output = use_case._SearchCastMembersUseCase__to_output( # pylint: disable=protected-access
        result=result
    )

    assert output == SearchCastMemberOutput(
        items=[],
        total=0,
        current_page=1,
        last_page=0,
        per_page=2,
        sort=None,
        sort_direction=None,
        filters=None,
    )


@pytest.mark.unit
def test_to_output_with_castmember():
    entity = CastMember(name="foo", kind=1)
    default_props = {
        "total": 1,
        "current_page": 1,
        "per_page": 2,
        "sort": None,
        "sort_direction": None,
        "filters": None,
    }

    result = CastMemberRepository.SearchResult(items=[entity], **default_props)
    repo = CastMemberInMemoryRepository()
    use_case = SearchCastMembersUseCase(repo)
    output = use_case._SearchCastMembersUseCase__to_output( # pylint: disable=protected-access
        result=result
    )

    items = [CastMemberOutputMapper.to_output(klass=CastMemberOutputDTO, castmember=entity)]
    assert output == PaginationOutputMapper.from_child(SearchCastMemberOutput).to_output(
        items, result
    )
