"""
Input para criar uma categoria
"""
# Python

# Apps
from kernel_catalogo_videos.core.application.dto import SearchInput
from kernel_catalogo_videos.core.domain.repositories import Filter
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository


class SearchCategoryInput(SearchInput[str]):
    pass
