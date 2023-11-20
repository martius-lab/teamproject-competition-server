from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import Protocol, ServerFactory
import sys

sys.path.insert(0, "")
from teamprojekt_competition_server.shared.commands import (
    AuthClient,
    StartGame,
    EndGame,
    Step,
)
from game import Game


class COMPServerProtocol(amp.AMP):
    game = None

    def connectionLost(self, reason):
        """handle everythin necessary when a client disconnects"""
        self.factory.client_disconnected(self)
        return super().connectionLost(reason)

    def auth_client(self, token, version):
        # TODO some auth handeling here, before we log the client as active

        self.factory.client_connected(
            self
        )  # log active clients after they authenticated
        print(f"--- Authentification --- \nToken: {token} | Version: {version}")
        self.factory.find_opponent(self)
        return {"uuid": 1111}  # dummy uuid

    AuthClient.responder(auth_client)

    def start_game(self, game: Game):
        self.game = game
        self.callRemote(StartGame, game_id=222).addCallback(lambda x: game.ready())

    def step(self):
        def answer(x):
            action = x.get("action")
            self.game.recieve_step(action=action)

        self.callRemote(Step, env=1).addCallback(answer)

    def end_game(self):
        self.callRemote(EndGame, result=True, stats=4).addCallback(lambda x: print(x))


class COMPServerFactory(ServerFactory):
    protocol = COMPServerProtocol
    player_queue = list()  # queue for storing agents waiting for a game
    active_clients = list()  # a basic list for storing logged in clients

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        protocol = COMPServerProtocol()
        protocol.factory = self
        return protocol

    def find_opponent(self, player: COMPServerProtocol):
        if len(self.player_queue) < 1:  # no players waiting
            self.player_queue.append(player)
        else:
            player1 = player
            player2 = self.player_queue.pop()
            game = Game(player1=player1, player2=player2)
            player1.start_game(game)
            player2.start_game(game)

    def client_connected(self, client):
        """add a newly connected client to the list of logged in clients"""
        self.active_clients.append(client)  # add new client
        # print('a client connected to the server.' )
        # print('currently there are ' + str(len(self.active_clients)) + ' active clients:')

    def client_disconnected(self, client):
        """remove a disconnected client from the list of logged in clients"""
        try:
            self.active_clients.remove(client)  # try to remove disconnected client
        except ValueError:
            pass
        # print('a client disconnected.' )
        # print('currently there are ' + str(len(self.active_clients)) + ' active clients:')
