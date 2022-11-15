# Python
from ast import In
from dataclasses import dataclass

# Third
import pytest

# Apps
from kernel_catalogo_videos.core.domain.entities import Entity
from kernel_catalogo_videos.core.domain.exceptions import NotFoundException
from kernel_catalogo_videos.core.domain.repositories import InMemoryRepository
from kernel_catalogo_videos.core.domain.unique_entity_id import UniqueEntityId


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: int


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


def make_repo():
    return StubInMemoryRepository()


@pytest.mark.unit
def test_items_prop_is_empty():
    repo = make_repo()
    assert repo.items == []


@pytest.mark.unit
def test_insert_entity():
    repo = make_repo()
    entity = StubEntity(name="some name", price=100)
    repo.insert(entity=entity)

    assert repo.items[0] == entity


@pytest.mark.unit
def test_raises_not_found_exception_when_fake_id():
    repo = make_repo()


    with pytest.raises(NotFoundException) as assert_error:
        repo.find_by_id('fake id')

    assert assert_error.value.args[0] == "Entity not found using ID 'fake id'"


@pytest.mark.unit
def test_raises_not_found_exception_when_not_found_entity():
    repo = make_repo()

    uuid = UniqueEntityId('dcc13d20-e91d-437d-a6ac-2fd60605a271')

    with pytest.raises(NotFoundException) as assert_error:
        repo.find_by_id(uuid)

    assert assert_error.value.args[0] == "Entity not found using ID 'dcc13d20-e91d-437d-a6ac-2fd60605a271'"


@pytest.mark.unit
def test_find_by_id():
    repo = make_repo()
    entity = StubEntity(name="some name", price=100)
    repo.insert(entity=entity)

    expected = repo.find_by_id(entity.id)

    assert expected == entity

    expected = repo.find_by_id(entity.unique_entity_id)
    assert expected == entity


def test_find_all():
    repo = make_repo()
    entity = StubEntity(name="some name", price=100)
    repo.insert(entity=entity)

    expected = repo.find_all()

    assert expected == [entity]


@pytest.mark.unit
def test_update_raises_not_found_exception_when_not_found_entity():
    repo = make_repo()

    uuid = UniqueEntityId('dcc13d20-e91d-437d-a6ac-2fd60605a271')

    entity = StubEntity(unique_entity_id=uuid, name="some name", price=100)

    with pytest.raises(NotFoundException) as assert_error:
        repo.update(entity)

    assert assert_error.value.args[0] == "Entity not found using ID 'dcc13d20-e91d-437d-a6ac-2fd60605a271'"


@pytest.mark.unit
def test_update():
    repo = make_repo()
    uuid = UniqueEntityId('dcc13d20-e91d-437d-a6ac-2fd60605a271')

    entity = StubEntity(unique_entity_id=uuid, name="some name", price=100)
    repo.insert(entity=entity)
    entity_update = StubEntity(unique_entity_id=uuid, name="name updated", price=200)

    repo.update(entity_update)

    assert repo.items[0] == entity_update



@pytest.mark.unit
def test_delete_raises_not_found_exception_when_fake_id():
    repo = make_repo()


    with pytest.raises(NotFoundException) as assert_error:
        repo.delete('fake id')

    assert assert_error.value.args[0] == "Entity not found using ID 'fake id'"


@pytest.mark.unit
def test_delete_raises_not_found_exception_when_not_found_entity():
    repo = make_repo()

    uuid = UniqueEntityId('dcc13d20-e91d-437d-a6ac-2fd60605a271')

    with pytest.raises(NotFoundException) as assert_error:
        repo.delete(uuid)

    assert assert_error.value.args[0] == "Entity not found using ID 'dcc13d20-e91d-437d-a6ac-2fd60605a271'"


@pytest.mark.unit
def test_delete():
    repo = make_repo()
    uuid = UniqueEntityId('dcc13d20-e91d-437d-a6ac-2fd60605a271')
    entity = StubEntity(unique_entity_id=uuid, name="some name", price=100)
    repo.insert(entity=entity)
    repo.delete(entity.id)

    assert repo.items == []
