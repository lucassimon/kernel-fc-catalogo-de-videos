# Python
from dataclasses import FrozenInstanceError, is_dataclass

# Third

import pytest


# Apps
from kernel_catalogo_videos.categories.domain import entities
from kernel_catalogo_videos.core.domain.exceptions import EntityValidationException
from kernel_catalogo_videos.core import utils


@pytest.mark.unit
def test_category_is_a_dataclass():
    assert is_dataclass(entities.Category) is True


@pytest.mark.unit
def test_category_constructor_default_params():
    data = dict(
        title="some test",
        slug="some-test",
    )

    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)
    assert category.title == data["title"]
    assert category.slug == data["slug"]


@pytest.mark.unit
def test_category_constructor():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=utils.ACTIVE_STATUS,
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)

    assert category.title == data["title"]
    assert category.slug == data["slug"]
    assert category.description == data["description"]
    assert category.status == data["status"]


@pytest.mark.unit
def test_is_immutable():
    data = dict(
        title="some test",
        slug="some-test",
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)
    with pytest.raises(FrozenInstanceError):
        category.title = "set name"


@pytest.mark.unit
def test_category_set_some_attribute():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=utils.ACTIVE_STATUS,
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)
    # pylint: disable=protected-access
    category._set("title", "new title")
    assert category.title == "new title"


@pytest.mark.unit
def test_category_activate():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=utils.INACTIVE_STATUS,
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)
    category.activate()
    assert category.status == utils.ACTIVE_STATUS


@pytest.mark.unit
def test_category_deactivate():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=utils.ACTIVE_STATUS,
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)
    category.deactivate()
    assert category.status == utils.INACTIVE_STATUS


@pytest.mark.unit
def test_category_update():
    data = dict(
        title="some test",
        slug="some-test",
        description="some description",
        status=utils.INACTIVE_STATUS,
    )
    # pylint: disable=unexpected-keyword-arg
    category = entities.Category(**data)

    new_data = dict(
        title="another title",
        slug="another-title",
        description="another-description",
    )
    category.update(data=new_data)

    assert category.title == new_data["title"]
    assert category.slug == new_data["slug"]
    assert category.description == new_data["description"]
