import pytest

from users.models import UserModel


@pytest.fixture(scope='function', autouse=True)
def clear_users(db_test):
    db_test.query(UserModel).delete()
    db_test.commit()
    yield
