"""Leaderboard page."""

import reflex as rx

from ..components import standard_layout
from ..protected_state import ProtectedState
from .. import reflex_local_auth


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def leaderboard() -> rx.Component:
    return standard_layout(
        rx.data_table(
            data=ProtectedState.ranked_users,
            columns=["Ranking", "Username", "µ / Σ"],
            search=True,
            sort=False,
            pagination=True,
        ),
        heading="Leaderboard",
    )
