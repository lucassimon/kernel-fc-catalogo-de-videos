# Python
import typing

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.repositories import Filter, SearchParams


@pytest.mark.unit
def test_props_annotations():
    assert SearchParams.__annotations__ == {
        "filters": typing.Optional[Filter],
        "page": typing.Optional[int],
        "per_page": typing.Optional[int],
        "sort": typing.Optional[str],
        "sort_direction": typing.Optional[str],
    }


@pytest.mark.unit
def test_page_props_when_default_equal_one():
    params = SearchParams()
    assert params.page == 1


@pytest.mark.unit
@pytest.mark.parametrize(
    "page, expected",
    [
        (None, 1),
        ("", 1),
        ("fake", 1),
        (0, 1),
        (-1, 1),
        ("0", 1),
        ("-1", 1),
        (5.5, 5),
        (True, 1),
        (False, 1),
        ({}, 1),
        (1, 1),
        (2, 2),
    ],
)
def test_page_props(page, expected):
    params = SearchParams(page=page)
    assert params.page == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "per_page, expected",
    [
        (None, 10),
        ("", 10),
        ("fake", 10),
        (0, 10),
        (-1, 10),
        ("0", 10),
        ("-1", 10),
        (5.5, 5),
        (True, 1),
        (False, 10),
        ({}, 10),
        (1, 1),
        (2, 2),
    ],
)
def test_per_page_props(per_page, expected):
    params = SearchParams(per_page=per_page)
    assert params.per_page == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "sort, expected",
    [
        (None, None),
        ("", None),
        ("fake", "fake"),
        (0, "0"),
        (-1, "-1"),
        ("0", "0"),
        ("-1", "-1"),
        (5.5, "5.5"),
        (True, "True"),
        (False, "False"),
        ({}, "{}"),
    ],
)
def test_sort_props(sort, expected):
    params = SearchParams(sort=sort)
    assert params.sort == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "sort_direction, expected",
    [
        (None, "asc"),
        ("", "asc"),
        ("fake", "asc"),
        (0, "asc"),
        (-1, "asc"),
        ("0", "asc"),
        ("-1", "asc"),
        (5.5, "asc"),
        (True, "asc"),
        (False, "asc"),
        ({}, "asc"),
        ("desc", "desc"),
        ("DESC", "desc"),
        ("ASC", "asc"),
        ("asc", "asc"),
    ],
)
def test_sort_direction_props(sort_direction, expected):
    params = SearchParams(sort="field", sort_direction=sort_direction)
    assert params.sort_direction == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "filters, expected",
    [
        (None, None),
        ("", None),
        ("fake", "fake"),
        (0, "0"),
        (-1, "-1"),
        ("0", "0"),
        ("-1", "-1"),
        (5.5, "5.5"),
        (True, "True"),
        (False, "False"),
        ({}, "{}"),
    ],
)
def test_filters_props(filters, expected):
    params = SearchParams(filters=filters)
    assert params.filters == expected
