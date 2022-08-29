import pytest


@pytest.fixture(scope='function')
def test_creation(db_test):
    def _test_creation(model):
        db_test.add(model)
        db_test.commit()
        assert model.id == 1

    return _test_creation
