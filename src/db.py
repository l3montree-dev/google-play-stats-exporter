from typing import Optional
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session
import model
from datetime import datetime
from log import logger
import csv


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

    def get_last_date_synced(self) -> Optional[datetime]:
        with self.session() as s:
            install = s.query(model.Install).order_by(
                model.Install.date.desc()).first()

            if install == None:
                return None
            return install.date

    def sync_stats(self, stats: list[str]):
        # installs, crashes, ratings
        with self.session() as s:
            for el in stats:

                if "installs" in el or "crashes" in el:
                    with open(el, encoding="utf-16") as f:
                        for row in csv.DictReader(f, skipinitialspace=True):
                            m = model.build_install_from_csv_row(
                                row) if "installs" in el else model.build_crash_from_csv_row(row)

                            s.add(m)
                            try:
                                s.commit()
                                logger.info("added: {}".format(el))
                            except (Exception) as e:
                                s.rollback()
                                logger.warn(
                                    "error during sql commit phase: {}".format(str(e.args[0])))
