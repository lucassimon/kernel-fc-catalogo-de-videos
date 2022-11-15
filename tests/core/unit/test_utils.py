# Third
import pytest

# Apps
from kernel_catalogo_videos.core import utils
from kernel_catalogo_videos.categories.domain import entities


@pytest.mark.unit
def test_check_is_inactive_or_deleted():
    """
    Check it is inactive or deleted
    """
    data = dict(title="some test", slug="some-test", is_deleted=False, status=utils.ACTIVE_STATUS)
    category = entities.Category(**data)

    data = dict(title="some test", slug="some-test", status=utils.INACTIVE_STATUS, is_deleted=True)
    category_inactive_and_deleted = entities.Category(**data)

    data = dict(title="some test", slug="some-test", status=utils.INACTIVE_STATUS, is_deleted=False)
    category_inactive = entities.Category(**data)

    data = dict(title="some test", slug="some-test", is_deleted=True)
    category_deleted = entities.Category(**data)

    assert utils.check_is_inactive_or_deleted(category) == False
    assert utils.check_is_inactive_or_deleted(category_inactive_and_deleted) == True
    assert utils.check_is_inactive_or_deleted(category_inactive) == True
    assert utils.check_is_inactive_or_deleted(category_deleted) == True

