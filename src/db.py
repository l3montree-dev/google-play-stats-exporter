import sqlalchemy
from sqlalchemy.orm import declarative_base
import model


def connect_to_db(user, password, host, port, db):
    engine = sqlalchemy.create_engine(
        'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'.format(user=user, password=password, host=host, port=port, db=db))
    session = sqlalchemy.orm.sessionmaker()
    session.configure(bind=engine)
    model.Base.metadata.create_all(engine)
