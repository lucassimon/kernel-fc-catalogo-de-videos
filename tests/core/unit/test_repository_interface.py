# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.repositories import RepositoryInterface


@pytest.mark.unit
def test_raise_not_implemented_error():

    with pytest.raises(TypeError) as assert_error:
        RepositoryInterface()

    assert assert_error.value.args[0] == (
        "Can't instantiate abstract class "
        "RepositoryInterface with abstract methods delete, "
        "find_all, find_by_id, insert, update"
    )
