"""Game overview.

List of all games of the logged in user.
"""

import reflex as rx

from ..components import standard_layout
from ..protected_state import UserGamesState, GameInfo
from .. import reflex_local_auth


def show_game(game: GameInfo) -> rx.Component:
    """Show a game in a table row."""
    return rx.table.row(
        rx.table.cell(game.player1),
        rx.table.cell(game.player2),
        rx.table.cell(game.result),
        rx.table.cell(game.time),
        rx.table.cell(game.id),
    )


def user_game_table() -> rx.Component:
    return rx.vstack(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.foreach(
                        UserGamesState.user_games_header, rx.table.column_header_cell
                    )
                ),
            ),
            rx.table.body(rx.foreach(UserGamesState.user_games, show_game)),
            on_mount=UserGamesState.load_user_games,
            width="100%",
        ),
        rx.hstack(
            rx.button(
                "Prev",
                on_click=UserGamesState.prev_page,
            ),
            rx.text(
                f"Page {UserGamesState.page_number} / {UserGamesState.total_pages}"
            ),
            rx.button(
                "Next",
                on_click=UserGamesState.next_page,
            ),
        ),
        rx.text(f"Games played: {UserGamesState.total_items}"),
    )


@rx.page(on_load=UserGamesState.on_load)
@reflex_local_auth.require_login
def game_overview() -> rx.Component:
    return standard_layout(
        rx.cond(
            UserGamesState.user_games,
            user_game_table(),
            rx.text("No games played yet."),
        ),
        heading="Games",
    )
