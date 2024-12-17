"""Main app module to demo local authentication."""

import dataclasses
from typing import Sequence

import reflex as rx
import sqlalchemy as sa

from comprl.server.data.sql_backend import Game, User

from . import reflex_local_auth
from .reflex_local_auth.local_auth import LocalAuthState, get_session


@dataclasses.dataclass
class GameStatistics:
    num_games_played: int = 0
    num_games_won: int = 0
    num_disconnects: int = 0


class ProtectedState(reflex_local_auth.LocalAuthState):
    data: str
    game_statistics: GameStatistics = GameStatistics()

    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        self.data = (
            "This is truly private data for"
            f" {LocalAuthState.authenticated_user.username}"
        )
        self.game_statistics = self._load_game_statistics()

    def do_logout(self):
        self.data = ""
        self.game_statistics = GameStatistics()
        return reflex_local_auth.LocalAuthState.do_logout

    def _load_game_statistics(self):
        stats = GameStatistics()
        with get_session() as session:
            stats.num_games_played = (
                session.query(Game)
                .filter(
                    sa.or_(
                        Game.user1 == self.authenticated_user.user_id,
                        Game.user2 == self.authenticated_user.user_id,
                    )
                )
                .with_entities(sa.func.count())
                .scalar()
            )

            stats.num_games_won = (
                session.query(Game)
                .filter(Game.winner == self.authenticated_user.user_id)
                .with_entities(sa.func.count())
                .scalar()
            )

            stats.num_disconnects = (
                session.query(Game)
                .filter(Game.disconnected == self.authenticated_user.user_id)
                .with_entities(sa.func.count())
                .scalar()
            )
        return stats

    def _get_ranked_users(self) -> Sequence[User]:
        with get_session() as session:
            stmt = sa.select(User).order_by((User.mu - User.sigma).desc())
            ranked_users = session.scalars(stmt).all()

        return ranked_users

    @rx.var
    def ranked_users(self) -> Sequence[tuple[int, str, str]]:
        return [
            (i + 1, user.username, f"{user.mu:.2f} / {user.sigma:.2f}")
            for i, user in enumerate(self._get_ranked_users())
        ]

    @rx.var
    def ranking_position(self) -> int:
        if not self.is_authenticated:
            return -1

        for i, user in enumerate(self._get_ranked_users()):
            if user.user_id == self.authenticated_user.user_id:
                return i + 1
        return -1


def links() -> rx.Component:
    """Render the links for the demo."""
    return rx.fragment(
        rx.link("Home", href="/"),
        rx.link("Dashboard", href="/dashboard"),
        rx.link("Leaderboard", href="/leaderboard"),
        rx.cond(
            reflex_local_auth.LocalAuthState.is_authenticated,
            rx.link(
                "Logout", href="/", on_click=reflex_local_auth.LocalAuthState.do_logout
            ),
            rx.link("Login", href=reflex_local_auth.routes.LOGIN_ROUTE),
        ),
    )


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


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def dashboard():
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


@rx.page(on_load=ProtectedState.on_load)
@reflex_local_auth.require_login
def leaderboard():
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
