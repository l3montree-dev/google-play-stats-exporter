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


def build_crash_from_csv_row(dict):
    return Crash(
        date=dict["Date"],
        package_name=dict["Package Name"],
        daily_crashes=dict["Daily Crashes"],
        daily_anrs=dict["Daily ANRs"],
    )


def build_install_from_csv_row(dict):
    return Install(
        date=dict["Date"],
        package_name=dict["Package Name"],
        daily_device_installs=dict["Daily Device Installs"],
        daily_device_uninstalls=dict["Daily Device Uninstalls"],
        daily_device_upgrades=dict["Daily Device Upgrades"],
        total_user_installs=dict["Total User Installs"],
        daily_user_installs=dict["Daily User Installs"],
        daily_user_uninstalls=dict["Daily User Uninstalls"],
        active_device_installs=dict["Active Device Installs"],
        install_events=dict["Install events"],
        update_events=dict["Update events"],
        uninstall_events=dict["Uninstall events"],
    )
