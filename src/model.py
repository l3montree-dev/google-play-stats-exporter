from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer

Base = declarative_base()


class Install(Base):
    __tablename__ = "installs"
    date = Column(Date, primary_key=True)
    package_name = Column(String(255))
    daily_device_installs = Column(Integer)
    daily_device_uninstalls = Column(Integer)
    daily_device_upgrades = Column(Integer)
    total_user_installs = Column(Integer)
    daily_user_installs = Column(Integer)
    daily_user_uninstalls = Column(Integer)
    active_device_installs = Column(Integer)
    install_events = Column(Integer)
    update_events = Column(Integer)
    uninstall_events = Column(Integer)


class Crash(Base):
    __tablename__ = "crashes"
    date = Column(Date, primary_key=True)
    package_name = Column(String(255))
    daily_crashes = Column(Integer)
    daily_anrs = Column(Integer)


class Rating(Base):
    __tablename__ = "ratings"
    date = Column(Date, primary_key=True)
    package_name = Column(String(255))
    daily_average_rating = Column(Integer)
    total_average_rating = Column(Integer)
