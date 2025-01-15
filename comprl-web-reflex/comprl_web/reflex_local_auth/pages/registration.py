"""An example registration page that can be used as-is.

app.add_page(
    reflex_local_auth.pages.register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)
"""

import reflex as rx

from .. import routes
from ..registration import RegistrationState
from .components import input_100w, MIN_WIDTH, PADDING_TOP


def register_error() -> rx.Component:
    """Render the registration error message."""
    return rx.cond(
        RegistrationState.error_message != "",
        rx.callout(
            RegistrationState.error_message,
            icon="triangle_alert",
            color_scheme="red",
            role="alert",
            width="100%",
        ),
    )


def register_form() -> rx.Component:
    """Render the registration form."""
    return rx.form(
        rx.vstack(
            rx.heading("Create an account", size="7"),
            register_error(),
            rx.text("Registration Key"),
            input_100w("key", placeholder="The key you got in the lecture"),
            rx.text(
                "Username (please use the pattern 'teamname-algorithm',"
                " e.g. 'team1-ppo')"
            ),
            input_100w("username", placeholder="teamname-algorithm"),
            rx.text("Password (Note: Password cannot be changed or recovered later)"),
            input_100w(
                "password", type="password", placeholder="Password (min. 8 chars)"
            ),
            rx.text("Repeat Password"),
            input_100w("confirm_password", type="password"),
            rx.button("Sign up", width="100%"),
            rx.center(
                rx.link("Login", on_click=lambda: rx.redirect(routes.LOGIN_ROUTE)),
                width="100%",
            ),
            min_width=MIN_WIDTH,
        ),
        on_submit=RegistrationState.handle_registration,
    )


def register_page() -> rx.Component:
    """Render the registration page.

    Returns:
        A reflex component.
    """

    return rx.center(
        rx.cond(
            RegistrationState.success,
            rx.vstack(
                rx.text("Registration successful!"),
            ),
            rx.card(register_form()),
        ),
        padding_top=PADDING_TOP,
    )
