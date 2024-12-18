"""Main app module to demo local authentication."""

import pathlib

import reflex as rx

from .components import standard_layout
from . import reflex_local_auth
from .pages import user_dashboard, leaderboard, games
from .reflex_local_auth.local_auth import LocalAuthState


def _validate_configuration() -> None:
    """Make sure the configuration is valid."""
    if not rx.config.get_config().comprl_registration_key:
        raise ValueError("Configuration: comprl_registration_key is not set.")

    if not pathlib.Path(rx.config.get_config().comprl_db_path).is_file():
        raise ValueError("Configuration: comprl_db_path does not exist.")


@rx.page()
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    index_page = rx.fragment(
        rx.cond(
            LocalAuthState.is_authenticated,
            rx.text(f"Hello {LocalAuthState.authenticated_user.username}"),
            reflex_local_auth.pages.login_page(),
        ),
        rx.text(f"Key: {rx.config.get_config().comprl_registration_key}"),
    )
    return standard_layout(index_page)


@rx.page(route=reflex_local_auth.routes.LOGIN_ROUTE)
def login() -> rx.Component:
    """Custom login page"""
    return standard_layout(reflex_local_auth.pages.login_page())


@rx.page(route=reflex_local_auth.routes.REGISTER_ROUTE, title="Register")
def registration() -> rx.Component:
    """Custom registration page"""
    return standard_layout(reflex_local_auth.pages.register_page())


_validate_configuration()

app = rx.App(theme=rx.theme(has_background=True, accent_color="teal"))
app.add_page(
    user_dashboard.dashboard,
    route="/dashboard",
    title="Dashboard",
)
app.add_page(
    leaderboard.leaderboard,
    route="/leaderboard",
    title="Leaderboard",
)
app.add_page(
    games.game_overview,
    route="/games",
    title="Games",
)
