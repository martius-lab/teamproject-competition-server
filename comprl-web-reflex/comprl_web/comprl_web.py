"""Main app module to demo local authentication."""

import reflex as rx

from .components import links
from . import reflex_local_auth
from .pages import user_dashboard, leaderboard
from .reflex_local_auth.local_auth import LocalAuthState


@rx.page()
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    return rx.fragment(
        rx.vstack(
            rx.heading("RL Competition", font_size="2em"),
            links(),
            rx.cond(
                LocalAuthState.is_authenticated,
                rx.text(f"Hello {LocalAuthState.authenticated_user.username}"),
                reflex_local_auth.pages.login_page(),
            ),
            spacing="2",
            padding_top="10%",
            align="center",
        ),
    )


@rx.page(route=reflex_local_auth.routes.LOGIN_ROUTE)
def login() -> rx.Component:
    """Custom login page"""
    return rx.fragment(
        rx.vstack(
            rx.heading("RL Competition", font_size="2em"),
            links(),
            reflex_local_auth.pages.login_page(),
            spacing="2",
            padding_top="10%",
            align="center",
        ),
    )

@rx.page(route=reflex_local_auth.routes.REGISTER_ROUTE, title="Register")
def registration() -> rx.Component:
    """Custom registration page"""
    return rx.fragment(
        rx.vstack(
            rx.heading("RL Competition", font_size="2em"),
            links(),
            reflex_local_auth.pages.register_page(),
            spacing="2",
            padding_top="10%",
            align="center",
        ),
    )


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
