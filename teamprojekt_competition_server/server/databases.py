import sqlite3

GAME_DB_NAME = "game_db"

class GameDatabase():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("teamprojekt_competition_server/server/COMP_database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{GAME_DB_NAME}'")
        print(self.cursor.fetchall())
        if self.cursor.fetchone() == None: 
            self.cursor.execute("CREATE TABLE game(player1, player2, win)")

    def insert_game(self, playerID1, playerID2, win: bool):
        self.cursor.execute(f"INSERT INTO game VALUES ({playerID1}, {playerID2}, {win})")
        self.connection.commit()
        return self.cursor.lastrowid


    def print_playerIDs(self):
        res = self.cursor.execute("SELECT rowid FROM game")
        players = res.fetchall()
        print(players)

    def get_playerIDs(self, gameID):
        res = self.cursor.execute(f"SELECT player1 FROM game WHERE rowid={gameID}")
        players = res.fetchall()
        return players