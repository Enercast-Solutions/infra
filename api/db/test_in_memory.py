import pytest
from .in_memory import InMemoryDBInterface


def test_create_or_update() -> None:
    db_ = InMemoryDBInterface()

    id = "test_id"
    obj = {"test_key": 10001, "test_key2": "test_value1"}

    db_.create_or_update(id, obj)

    assert id in db_.data
    assert obj == db_.data[id]


def test_get() -> None:
    db_ = InMemoryDBInterface()

    id = "test_id"
    obj = {"test_key": 10001, "test_key2": "test_value1"}

    db_.create_or_update(id, obj)

    resp = db_.get(id)

    assert resp == obj


def test_delete_fail() -> None:
    db_ = InMemoryDBInterface()

    with pytest.raises(ValueError):
        db_.delete("test_id")


def test_get_fail() -> None:
    db_ = InMemoryDBInterface()

    with pytest.raises(ValueError):
        db_.get("test_id")
