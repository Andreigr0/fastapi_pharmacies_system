from users import crud
from users.schemas import UserCreate


def test_create_user(db_test):
    user = UserCreate(email='test_user_asdf@test.com', login='login', password='password')
    created = crud.create_user(db=db_test, user=user)
    assert created.login == user.login
    assert created.email == user.email
    assert created.hashed_password != user.password


def test_get_users(db_test):
    user1 = UserCreate(email='test_user1@test.com', login='login1', password='password')
    user2 = UserCreate(email='test_user2@test.com', login='login2', password='password')
    crud.create_user(db_test, user1)
    crud.create_user(db_test, user2)

    users = crud.get_users(db_test)
    assert len(users) == 2
