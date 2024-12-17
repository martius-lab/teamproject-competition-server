"""User dashboard page."""

import reflex as rx

from ..components import links
from ..protected_state import ProtectedState
from .. import reflex_local_auth
from ..reflex_local_auth.local_auth import LocalAuthState


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def dashboard() -> rx.Component:
    win_rate = round(
        ProtectedState.game_statistics.num_games_won
        / ProtectedState.game_statistics.num_games_played
        * 100
    )
    return rx.vstack(
        rx.heading("Dashboard"),
        links(),
        rx.card(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label("username"),
                    rx.data_list.value(LocalAuthState.authenticated_user.username),
                ),
                rx.data_list.item(
                    rx.data_list.label("Access Token"),
                    rx.data_list.value(LocalAuthState.authenticated_user.token),
                ),
                rx.data_list.item(
                    rx.data_list.label("Ranking"),
                    rx.data_list.value(f"{ProtectedState.ranking_position}. place"),
                ),
                rx.data_list.item(
                    rx.data_list.label("Games Played"),
                    rx.data_list.value(ProtectedState.game_statistics.num_games_played),
                ),
                rx.data_list.item(
                    rx.data_list.label("Games Won"),
                    rx.data_list.value(ProtectedState.game_statistics.num_games_won),
                ),
                rx.data_list.item(
                    rx.data_list.label("Win rate"),
                    rx.data_list.value(f"{win_rate} %"),
                ),
                rx.data_list.item(
                    rx.data_list.label("Disconnects"),
                    rx.data_list.value(ProtectedState.game_statistics.num_disconnects),
                ),
            ),
        ),
        spacing="2",
        padding_top="10%",
        align="center",
    )
