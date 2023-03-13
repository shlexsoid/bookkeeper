from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass

import pytest

@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        name: str = 'zero'
    return Custom

@pytest.fixture
def repo(custom_class):
    return SQLiteRepository('test_db.db', custom_class)

def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None

def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = None
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_delete_unexistent(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    with pytest.raises(KeyError):
        repo.delete(pk + 10)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)
