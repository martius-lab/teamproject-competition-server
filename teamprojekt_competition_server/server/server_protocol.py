from collections import deque
import json

from typing import Optional
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

    def auth_client(self, token, version):
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
    queue = deque()  # queue for storing agents waiting for a game

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        protocol = COMPServerProtocol()
        protocol.factory = self
        return protocol

    def find_opponent(self, player: COMPServerProtocol):
        if len(self.queue) < 1:  # no players waiting
            self.queue.append(player)
        else:
            player1 = player
            player2 = self.queue.pop()
            game = Game(player1=player1, player2=player2)
            player1.start_game(game)
            player2.start_game(game)
