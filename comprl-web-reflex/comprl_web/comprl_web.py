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
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to my homepage!", font_size="2em"),
            rx.cond(
                LocalAuthState.is_authenticated,
                rx.heading(f"Hello {LocalAuthState.authenticated_user.username}"),
                rx.box(),
            ),
            links(),
            spacing="2",
            padding_top="10%",
            align="center",
        ),
    )


app = rx.App(theme=rx.theme(has_background=True, accent_color="orange"))
app.add_page(
    reflex_local_auth.pages.login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(
    reflex_local_auth.pages.register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)
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
