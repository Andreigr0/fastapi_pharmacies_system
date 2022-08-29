from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


def todict(obj):
    """ Return the object's dict excluding private attributes,
    sqlalchemy state and relationship attributes.
    """
    excl = ('_sa_adapter', '_sa_instance_state')
    return {k: v for k, v in vars(obj).items() if not k.startswith('_') and
            not any(hasattr(v, a) for a in excl)}


class Base:
    def __repr__(self):
        params = ', '.join(f'{k}={v}' for k, v in todict(self).items())
        return f"{self.__class__.__name__}({params})"


Base = declarative_base(cls=Base)


@lru_cache()
def get_settings():
    from app.core.config import Settings
    return Settings()


def setup_engine() -> Engine:
    return create_engine(get_settings().DATABASE_URI)


def setup_db(engine: Engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    from app.main import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
