from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from eNMS.controller.config import config

DATABASE_URL = environ.get(
    "DATABASE_URL", "sqlite:///database.db?check_same_thread=False"
)
DIALECT = DATABASE_URL.split(":")[0]

engine_parameters = {
    "convert_unicode": True,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}

if DIALECT == "mysql":
    engine_parameters.update(
        {
            "max_overflow": int(environ.get("MAX_OVERFLOW", 10)),
            "pool_size": int(environ.get("POOL_SIZE", 1000)),
        }
    )

engine = create_engine(
    environ.get("DATABASE_URL", "sqlite:///database.db?check_same_thread=False"),
    **engine_parameters
)
Session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()
