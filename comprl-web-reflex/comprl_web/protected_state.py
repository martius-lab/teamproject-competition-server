"""State for the protected pages."""
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
