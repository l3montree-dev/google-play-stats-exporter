import sqlalchemy
from sqlalchemy.orm import declarative_base


Base = declarative_base()


def connect_to_db():
    engine = sqlalchemy.create_engine(
        'dialect+driver://user:pass@host:port/db')
