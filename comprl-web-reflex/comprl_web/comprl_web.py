"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


from .base_state import State
from .login import require_login
from .registration import registration_page


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link("Protected Page", href="/protected"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


@require_login
def protected() -> rx.Component:
    """Render a protected page.

    The `require_login` decorator will redirect to the login page if the user is
    not authenticated.

    Returns:
        A reflex component.
    """
    return rx.vstack(
        rx.heading(
            "Protected Page for ", State.authenticated_user.username, font_size="2em"
        ),
        rx.link("Home", href="/"),
        rx.link("Logout", href="/", on_click=State.do_logout),
    )


app = rx.App()
app.add_page(index)
app.add_page(protected)
