"""
Output retornando os dados de uma categoria
"""
# pylint: disable=duplicate-code

# Python
from typing import TypeVar, Optional
from datetime import datetime
from dataclasses import dataclass

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre


@dataclass(slots=True, frozen=True)
class GenreOutputDTO:
    id: str  # pylint: disable=invalid-name
    title: str
    slug: str
    is_deleted: bool
    created_at: datetime
    status: Optional[int] = 1


Output = TypeVar("Output", bound=GenreOutputDTO)


class GenreOutputMapper:
    @staticmethod
    def to_output(klass: Output, genre: Genre) -> Output:
        return klass(
            id=genre.id,
            title=genre.title,
            slug=genre.slug,
            status=genre.status,
            is_deleted=genre.is_deleted,
            created_at=genre.created_at,
        )
