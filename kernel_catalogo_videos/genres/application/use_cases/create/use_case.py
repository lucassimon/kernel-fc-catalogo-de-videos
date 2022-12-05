"""
Caso de uso para criar uma categoria
"""
# Python
from logging import Logger
from dataclasses import asdict

# Apps
from kernel_catalogo_videos.genres.domain.entities import Genre
from kernel_catalogo_videos.core.application.use_case import UseCase
from kernel_catalogo_videos.genres.domain.repositories import GenreRepository
from kernel_catalogo_videos.genres.application.use_cases.dto import GenreOutputMapper
from kernel_catalogo_videos.genres.application.use_cases.create.input import CreateGenreInput
from kernel_catalogo_videos.genres.application.use_cases.create.output import CreateGenreOutput


class CreateGenreUseCase(UseCase[CreateGenreInput, CreateGenreOutput]):
    """
    Classe para criar um genero
    """

    repo: GenreRepository

    def __init__(self, repo: GenreRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def execute(self, input_params: CreateGenreInput) -> CreateGenreOutput:
        if self.logger:
            self.logger.info("create.genre.usecase", message="Initial Payload", input_params=asdict(input_params))

        genre = Genre(
            title=input_params.title,
            status=input_params.status,
        )
        genre.normalize()

        if self.logger:
            self.logger.info("create.genre.usecase", message="Entity created", genre=genre.to_dict())

        self.repo.insert(genre)
        if self.logger:
            self.logger.info("create.genre.usecase", message="Entity saved")

        return self.__to_output(genre=genre)

    def __to_output(self, genre: Genre):
        return GenreOutputMapper.to_output(klass=CreateGenreOutput, genre=genre)
