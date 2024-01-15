import teamprojekt_competition_server.server.game_database as game_db
import logging

logging.basicConfig(level=logging.DEBUG)

def database_tests():
    gameID1 = game_db.insert_won_game(
        winner_id=23, loser_id=4, score_winner=3, score_loser=6
    )
    gameID2 = game_db.insert_won_game(
        winner_id=43,
        loser_id=23,
        score_winner=6,
        score_loser=7,
    )
    gameID3 = game_db.insert_disconnected_game(
        disconnected_user_id=1,
        other_user_id=23,
        score_disconnected_user=6,
        score_other_user=7,
    )
    
    print(gameID1, gameID2, gameID3)
    assert gameID1 % 3 == 1 and gameID2 % 3 == 2 and gameID3 % 3 == 0 
    assert game_db.get_user_ids(game_id=gameID2) == (43, 23)
    assert game_db.win_rate(user_id=23) == 0.5
    assert len(game_db.get_game_ids(user_id=23)) % 3 == 0
    assert len(game_db.get_won_game_ids(user_id=23)) == len(game_db.get_game_ids(user_id=23))/3
    assert game_db.count_played_games(user_id=23) % 3 == 0
    assert game_db.count_won_games(user_id=23) == game_db.count_played_games(user_id=23)/3
    assert game_db.count_disconnected_games(user_id=23) == 0
    assert game_db.count_games_with_disconnect(user_id=23) == game_db.count_played_games(user_id=23)/3
    

if __name__ == "__main__":
    database_tests() # only enable for manual testing


