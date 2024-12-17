"""Leaderboard page."""

import reflex as rx

from ..components import links
from ..protected_state import ProtectedState
from .. import reflex_local_auth


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def leaderboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Leaderboard"),
        links(),
        rx.data_table(
            data=ProtectedState.ranked_users,
            columns=["Ranking", "Username", "µ / Σ"],
            search=True,
            sort=False,
        ),
        spacing="2",
        padding_top="10%",
        align="center",
    )
