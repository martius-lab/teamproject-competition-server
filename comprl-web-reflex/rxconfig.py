import reflex as rx


class CustomConfig(rx.Config):
    # path to comprl config file
    comprl_config_path: str = ""


config = CustomConfig(
    app_name="comprl_web",
    telemetry_enabled=False,
)
