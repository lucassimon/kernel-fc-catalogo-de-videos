# Third
import pytest

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre

@pytest.mark.unit
def test_create_entity_successfully():
    genre = Genre(title="foo", slug="foo")

    assert genre.title == "foo"
    assert genre.slug == "foo"



