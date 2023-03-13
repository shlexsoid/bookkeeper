import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget

@pytest.fixture
def repo():
    return MemoryRepository()

def test_create_with_full_args_list():
    b = Budget(amount=1, category=1, time=1, limit=100, pk=1)
    assert b.amount == 1
    assert b.category == 1
    assert b.time == 1
    assert b.limit == 100


def test_create_brief():
    b = Budget(1, 1, 1)
    assert b.amount == 1
    assert b.category == 1
    assert b.time == 1


def test_can_add_to_repo(repo):
    b = Budget(1, 2, 3)
    pk = repo.add(b)
    assert b.pk == pk