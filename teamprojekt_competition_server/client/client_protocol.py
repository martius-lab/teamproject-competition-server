from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import ClientFactory, Protocol
import sys

sys.path.insert(0, "")
from teamprojekt_competition_server.shared.commands import StartGame, EndGame, Step


class COMPClientProtocol(amp.AMP):
    def connectionMade(self):
        return super().connectionMade()

    def connectionLost(self, reason):
        return super().connectionLost(reason)

    def start_game(self, game_id):
        print(f"--- Started Game --- \nGame ID: {game_id}")
        return {"ready": True}  # dummy ready

    StartGame.responder(start_game)

    def end_game(self, result, stats):
        print(f"--- Ended Game --- \nGame ID: {result} | Stats: {stats}")
        return {"ready": True}  # dummy ready

    EndGame.responder(end_game)

    def step(self, env):
        action = int(input("Enter a move: "))  # dummy action
        print(f"--- Next Step --- \nEnviroment: {env} | Action: {action}")
        return {"action": action}

    Step.responder(step)


class COMPClientFactory(ClientFactory):
    def startFactory(self):
        pass

    def stopFactory(self):
        pass

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        return COMPClientProtocol()
