import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

DB_FILE = "cars.db" # TODO do configu

db_engine = create_engine(f"sqlite+pysqlite:///{DB_FILE}", echo=False)
global_session = sessionmaker(bind=db_engine)


if not os.path.isfile(DB_FILE):
    Base.metadata.create_all(db_engine)


def session_manager():
    """Context manager pro řízení session v DB."""
    session = global_session()
    try:
        yield session
        session.commit()
    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()




