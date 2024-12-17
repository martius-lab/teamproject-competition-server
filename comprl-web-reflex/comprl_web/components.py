"""Components used on multiple pages."""

import reflex as rx

from .reflex_local_auth.local_auth import LocalAuthState
from .reflex_local_auth import routes


def links() -> rx.Component:
    """Render the links for the demo."""
    return rx.fragment(
        rx.link("Home", href="/"),
        rx.link("Dashboard", href="/dashboard"),
        rx.link("Leaderboard", href="/leaderboard"),
        rx.cond(
            LocalAuthState.is_authenticated,
            rx.link("Logout", href="/", on_click=LocalAuthState.do_logout),
            rx.link("Login", href=routes.LOGIN_ROUTE),
        ),
    )
