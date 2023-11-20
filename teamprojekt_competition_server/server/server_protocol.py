"""class for server protocol"""
import sys

from collections import deque
from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import Protocol, ServerFactory

from teamprojekt_competition_server.shared.commands import (
    AuthClient,
    StartGame,
    EndGame,
    Step,
)
from game import Game

sys.path.insert(0, "")


class COMPServerProtocol(amp.AMP):
    """amp protocol for a COMP server"""

    game = None

    def auth_client(self, token: str, version):
        """is called when a client wants to authenticate itself

        Args:
            token (str): token to authenticate the client
            version (int): current version of the client

        Returns:
            {"uuid": int}: unique client ID
        """
        print(f"--- Authentification --- \nToken: {token} | Version: {version}")
        self.factory.find_opponent(self)
        return {"uuid": 1111}  # dummy uuid

    AuthClient.responder(auth_client)

    def start_game(self, game: Game):
        """starts the game

        Args:
            game (Game): game that starts
        """
        self.game = game
        self.callRemote(StartGame, game_id=222).addCallback(lambda x: game.ready())

    def step(self, env):
        """perfroms step requested by player"""

        def answer(x):
            action = x.get("action")
            self.game.receive_step(action=action)

        self.callRemote(Step, env=int(env)).addCallback(answer)

    def end_game(self):
        """ends the game"""
        self.callRemote(EndGame, result=True, stats=4).addCallback(lambda x: print(x))


class COMPServerFactory(ServerFactory):
    """factory for COMP servers"""

    protocol = COMPServerProtocol
    queue = deque()  # queue for storing agents waiting for a game

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """builds the protocoll"""
        protocol = COMPServerProtocol()
        protocol.factory = self
        return protocol

    def find_opponent(self, player: COMPServerProtocol):
        """addes the player to a queue in order to match two players
        Args:
            player (COMPServerProtocol): player that wants to find an opponent
        """
        if len(self.queue) < 1:  # no players waiting
            self.queue.append(player)
        else:
            player1 = player
            player2 = self.queue.pop()
            game = Game(player1=player1, player2=player2)
            player1.start_game(game)
            player2.start_game(game)
