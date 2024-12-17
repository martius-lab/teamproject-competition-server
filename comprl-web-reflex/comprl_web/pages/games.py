"""Game overview.

List of all games of the logged in user.
"""

import reflex as rx

from ..components import standard_layout
from ..protected_state import ProtectedState
from .. import reflex_local_auth


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def game_overview() -> rx.Component:
    return standard_layout(
        rx.cond(
            ProtectedState.user_games,
            rx.data_table(
                data=ProtectedState.user_games,
                columns=ProtectedState.user_games_header,
                search=True,
                pagination=True,
            ),
            rx.text("No games played yet."),
        ),
        heading="Games",
    )
