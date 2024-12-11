import sqlite3
import uuid

import pytest

from comprl.server.data.interfaces import GameEndState, GameResult
from comprl.server.data import ConnectionInfo, GameData


def test_game_data(tmp_path):
    db_file = tmp_path / "users.db"
    table_name = "games"
    game_data = GameData(ConnectionInfo(host=db_file, table=table_name))

    # add some test games
    game1_uuid = uuid.uuid4()
    game2_uuid = uuid.uuid4()
    game3_uuid = uuid.uuid4()
    game4_uuid = uuid.uuid4()
    game_data.add(
        GameResult(
            game_id=game1_uuid,
            user1_id=1,
            user2_id=2,
            score_user_1=3,
            score_user_2=6,
        )
    )
    game_data.add(
        GameResult(
            game_id=game2_uuid,
            user1_id=1,
            user2_id=2,
            score_user_1=3,
            score_user_2=6,
            start_time="2021-01-01 12:00:00",
            end_state=GameEndState.DRAW,
        )
    )
    game_data.add(
        GameResult(
            game_id=game3_uuid,
            user1_id=1,
            user2_id=2,
            score_user_1=3,
            score_user_2=6,
            start_time="2021-01-01 13:00:00",
            end_state=GameEndState.WIN,
            is_user1_winner=True,
        )
    )
    game_data.add(
        GameResult(
            game_id=game4_uuid,
            user1_id=1,
            user2_id=2,
            score_user_1=3,
            score_user_2=6,
            start_time="2021-01-01 13:00:00",
            end_state=GameEndState.DISCONNECTED,
            is_user1_disconnected=True,
        )
    )

    # check that I can't add two games with same ID
    with pytest.raises(sqlite3.IntegrityError):
        game_data.add(
            GameResult(
                game_id=game1_uuid,
                user1_id=1,
                user2_id=2,
                score_user_1=3,
                score_user_2=6,
            )
        )

    # NOTE: There are currently no methods to retrieve any information about games from
    # the database, so no further checks can be done here.
