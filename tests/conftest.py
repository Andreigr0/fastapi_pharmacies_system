import logging
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import get_db, Base

logger = logging.getLogger(__name__)
sqlite_path = f'{Path(__file__).parent}/test.db'
# DB_URI = f'sqlite://{sqlite_path}'
# DB_URI = 'sqlite://'
DB_URI = 'postgresql://postgres:postgrespw@localhost:55001/postgres'


@pytest.fixture(scope="session")
def monkey_session():
    from _pytest.monkeypatch import MonkeyPatch
    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@pytest.fixture(scope='session')
def testing_engine():
    return create_engine(DB_URI)


@pytest.fixture(scope='session', autouse=True)
def apply_migrations(monkey_session, testing_engine):
    class _MockSettings(BaseSettings):
        DATABASE_URI = DB_URI

    def _get_settings():
        return _MockSettings()

    monkey_session.setattr('app.database.get_settings', _get_settings)
    import alembic.config
    os.chdir(Path(__file__).parent.parent)
    alembic.config.main(argv=['upgrade', 'head'])
    yield
    Base.metadata.drop_all(bind=testing_engine)
    print('🤔🤔🤔')


@pytest.fixture(scope='session', autouse=True)
def faker_locale():
    return ['ru_RU']


@pytest.fixture(scope='session')
def get_db_override(testing_engine):
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)

    def _get_db() -> Session:
        db: Session = TestingSession()
        try:
            yield db
        finally:
            db.close()

    return _get_db


@pytest.fixture(scope='session')
def db_test(get_db_override):
    yield from get_db_override()


@pytest.fixture(scope='session')
def test_client(get_db_override, testing_engine, monkey_session):
    def _testing_engine():
        return testing_engine

    monkey_session.setattr('app.database.setup_engine', _testing_engine)
    from app.main import app
    app.dependency_overrides[get_db] = get_db_override
    return TestClient(app)
