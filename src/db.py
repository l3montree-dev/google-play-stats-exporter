from typing import Optional
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session
import model
from datetime import datetime
from log import logger
import csv
from builder import Builder


class DbHandler():
    session: Session

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        db: str
    ):
        engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{user}:{password}@{host}:{port}/{db}'.format(user=user, password=password, host=host, port=port, db=db))
        session = sqlalchemy.orm.sessionmaker(engine)
        model.Base.metadata.create_all(engine)
        self.session = session

    def get_last_date_synced(self, m: Builder) -> Optional[datetime]:
        with self.session() as s:
            latest_model = s.query(m.get_model()).order_by(
                m.get_model().date.desc()).first()

            if latest_model == None:
                return None
            return latest_model.date

    def sync_stats(self, stats: list[str], builder: Builder):
        with self.session() as s:
            for el in stats:
                with open(el, encoding="utf-16") as f:
                    for row in csv.DictReader(f, skipinitialspace=True):
                        m = builder.build_from_csv_row(row)
                        s.merge(m)
                        try:
                            s.commit()
                            logger.info("added: {}".format(el))
                        except (Exception) as e:
                            s.rollback()
                            logger.warn(
                                "error during sql commit phase: {}".format(str(e.args[0])))
