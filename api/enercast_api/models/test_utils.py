from .utils import generate_id


def test_generate_id_pass() -> None:
    assert type(generate_id()) == str
