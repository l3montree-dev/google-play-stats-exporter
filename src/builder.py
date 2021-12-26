from abc import abstractclassmethod


import model


class Builder():
    @abstractclassmethod
    def build_from_csv_row(self, dict) -> model.Base:
        pass

    @abstractclassmethod
    def get_model(self) -> model.Base:
        pass

    @abstractclassmethod
    def get_prefix(self) -> str:
        pass


class CrashBuilder(Builder):
    def build_from_csv_row(self, dict) -> model.Base:
        return model.Crash(
            date=dict["Date"],
            package_name=dict["Package Name"],
            daily_crashes=dict["Daily Crashes"],
            daily_anrs=dict["Daily ANRs"],
        )

    def get_model(self) -> model.Base:
        return model.Crash

    def get_prefix(self) -> str:
        return "crashes"


class RatingBuilder(Builder):
    def get_prefix(self) -> str:
        return "ratings"

    def build_from_csv_row(self, dict) -> model.Base:
        return model.Rating(
            date=dict["Date"],
            package_name=dict["Package Name"],
            daily_average_rating=0 if dict["Daily Average Rating"] == "NA" else dict["Daily Average Rating"],
            total_average_rating=dict["Total Average Rating"],
        )

    def get_model(self) -> model.Base:
        return model.Rating


class InstallBuilder(Builder):
    def get_prefix(self) -> str:
        return "installs"

    def build_from_csv_row(self, dict) -> model.Base:
        return model.Install(
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

    def get_model(self) -> model.Base:
        return model.Install
