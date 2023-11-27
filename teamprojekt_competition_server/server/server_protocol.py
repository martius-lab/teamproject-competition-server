"""class for server protocol"""

from typing import cast, List
from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import Protocol, ServerFactory

from ..shared.commands import (
    AuthClient,
    StartGame,
    EndGame,
    Step,
)

from .game import Game


class COMPServerProtocol(amp.AMP):
    """amp protocol for a COMP server"""

    game = None

    def __init__(self, factory, boxReceiver=None, locator=None):
        self.factory = factory
        super().__init__(boxReceiver, locator)

    def connectionLost(self, reason):
        """is called when a client disconnects"""
        cast(
            COMPServerFactory, self.factory
        ).client_disconnected(  # keep track of the logged in clients
            self
        )  # TODO: this is really really, like ultra hacky !!!!
        return super().connectionLost(reason)

    def auth_client(self, token: str, version):
        """is called when a client wants to authenticate itself

        Args:
            token (str): token to authenticate the client
            version (int): current version of the client

        Returns:
            {"uuid": int}: unique client ID
        """

        # TODO: Auth. the client

        print(f"--- Authentification --- \nToken: {token} | Version: {version}")

        cast(
            COMPServerFactory, self.factory
        ).client_connected(  # keep track of the (auth.) connected clients
            self
        )  # TODO: this is really really, like ultra hacky !!!!

        cast(COMPServerFactory, self.factory).find_opponent(
            self
        )  # TODO: this is really really, like ultra hacky !!!!

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

    # a basic list for storing logged in clients
    active_clients: List[COMPServerProtocol] = []
    # queue for storing agents waiting for a game
    player_queue: List[COMPServerProtocol] = []

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """builds the protocoll"""
        protocol = COMPServerProtocol(factory=self)
        return protocol

    def find_opponent(self, player: COMPServerProtocol):
        """addes the player to a queue in order to match two players
        Args:
            player (COMPServerProtocol): player that wants to find an opponent
        """
        if len(self.player_queue) < 1:  # no players waiting
            self.player_queue.append(player)
        else:
            player1 = player
            player2 = self.player_queue.pop()
            game = Game(player1=player1, player2=player2)
            player1.start_game(game)
            player2.start_game(game)

    def client_connected(self, client: COMPServerProtocol):
        """add a newly connected client to the list of logged in clients

        Args:
            client (COMPServerProtocol): the client that connected
        """
        self.active_clients.append(client)  # add new client
        # print("a client connected to the server.")
        # print("currently there are " + str(len(self.active_clients))
        # + " active clients:")

    def client_disconnected(self, client: COMPServerProtocol):
        """remove a disconnected client from the list of logged in clients

        Args:
            client (COMPServerProtocol): the client that disconnected
        """
        try:
            self.active_clients.remove(client)  # try to remove disconnected client
        except ValueError:
            pass
        # print("a client disconnected.")
        # print("currently there are " + str(len(self.active_clients))
        # + " active clients:")
