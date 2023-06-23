import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
import config


db_engine = create_engine(f"{config.DB_DRIVER}:///{config.DB_URL}", echo=False)
global_session = sessionmaker(bind=db_engine)


if config.DB_DRIVER == "sqlite+pysqlite" and not os.path.isfile(config.DB_URL):
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




