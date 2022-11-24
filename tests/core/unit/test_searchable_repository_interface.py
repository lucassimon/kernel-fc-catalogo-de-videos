# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.repositories import (
    Filter,
    SearchParams,
    SearchableRepositoryInterface,
)


@pytest.mark.unit
def test_raise_not_implemented_error():

    with pytest.raises(TypeError) as assert_error:
        SearchableRepositoryInterface()

    assert assert_error.value.args[0] == (
        "Can't instantiate abstract class "
        "SearchableRepositoryInterface with abstract methods delete, "
        "find_all, find_by_id, insert, search, update"
    )


@pytest.mark.unit
def test_sortable_fields_prop():
    assert SearchableRepositoryInterface.sortable_fields == []
