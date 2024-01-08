import sqlite3

GAME_DB_NAME = "game"

class GameDatabase():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("teamprojekt_competition_server/server/COMP_database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{GAME_DB_NAME}'")
        if self.cursor.fetchone() == None: 
            self.cursor.execute(f"CREATE TABLE {GAME_DB_NAME}(winnerID, loserID)")

    def insert_game(self, winnerID, loserID):
        self.cursor.execute(f"INSERT INTO game VALUES ({winnerID}, {loserID})")
        self.connection.commit()
        return self.cursor.lastrowid

    def get_playerIDs(self, gameID):
        res = self.cursor.execute(f"SELECT winnerID, loserID FROM {GAME_DB_NAME} WHERE rowid={gameID}")
        players = res.fetchone()
        return players
    
    def get_gameIDs(self, playerID):
        res = self.cursor.execute(f"SELECT rowid FROM {GAME_DB_NAME} WHERE winnerID={playerID} OR loserID={playerID}")
        games = res.fetchall()
        return games
    
    def get_won_gameIDs(self, playerID):
        res = self.cursor.execute(f"SELECT rowid FROM {GAME_DB_NAME} WHERE winnerID={playerID}")
        games = res.fetchall()
        return games