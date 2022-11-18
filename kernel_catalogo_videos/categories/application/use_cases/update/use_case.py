"""
Caso de uso para atualizar uma categoria
"""


# Apps
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.categories.domain.entities import Category
from kernel_catalogo_videos.categories.domain.repositories import CategoryRepository
from kernel_catalogo_videos.categories.application.use_cases.dto import CategoryOutputMapper
from kernel_catalogo_videos.categories.application.use_cases.update.input import UpdateCategoryInput
from kernel_catalogo_videos.categories.application.use_cases.update.output import UpdateCategoryOutput


class UpdateCategoryUseCase(UseCase[UpdateCategoryInput, UpdateCategoryOutput]):
    """
    Atualizar uma categoria
    """
    repo: CategoryRepository

    def __init__(self, repo: CategoryRepository) -> None:
        self.repo = repo

    def execute(self, input_param: UpdateCategoryInput) -> UpdateCategoryOutput:
        entity = self.repo.find_by_id(input_param.id)
        entity.update(input_param.name, input_param.description)

        if input_param.is_active is True:
            entity.activate()

        if input_param.is_active is False:
            entity.deactivate()

        return self.__to_output(category=entity)

    def __to_output(self, category: Category):
        # TODO: Utilizar o Output do create
        return CategoryOutputMapper.to_output(klass=UpdateCategoryOutput, category=category)
