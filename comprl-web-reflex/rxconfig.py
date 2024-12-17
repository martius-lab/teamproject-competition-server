import reflex as rx


class CustomConfig(rx.Config):
    # path tot he comprl database
    comprl_db_path: str = ""
    # key that has to be specified to register
    comprl_registration_key: str = ""


config = CustomConfig(
    app_name="comprl_web",
    telemetry_enabled=False,
)
