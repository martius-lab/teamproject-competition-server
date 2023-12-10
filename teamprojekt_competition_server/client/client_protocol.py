"""class for client protocol"""

from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import ClientFactory, Protocol

from ..shared.commands import StartGame, EndGame, Step, Auth


class COMPClientProtocol(amp.AMP):
    """protocol for the client"""

    token: str = "Unknown"

    def __init__(self, agent, token, boxReceiver=None, locator=None):
        super().__init__(boxReceiver, locator)
        self.agent = agent
        self.token = token

    def start_game(self, game_id: int):
        """is called when the server starts the game

        Args:
            game_id (int): ID of the game

        Returns:
            {"ready": boolean}: true if the client is ready to start the game
        """
        print(f"--- Started Game --- \nGame ID: {game_id}")
        return {"ready": True}  # dummy ready

    StartGame.responder(start_game)

    def end_game(self, result, stats):
        """is called when the server ends the game

        Args:
            result (boolean): if the game was won
            stats (_type_): other statistics

        Returns:
            {"ready": boolean}: true if the client is ready to start a new game
        """
        print(f"--- Ended Game --- \nGame ID: {result} | Stats: {stats}")
        return {"ready": True}  # dummy ready

    EndGame.responder(end_game)

    def step(self, env):
        """is called when the server wants the client to make a step

        Args:
            env (int): enviroment given by the server

        Returns:
            {"action": int}: action that should be executed
        """
        action = self.agent.step(env=int(env))  # dummy action
        print(f"--- Next Step --- \nEnviroment: {env} | Action: {action}")
        return {"action": action}

    Step.responder(step)

    def auth(self):
        """called for auth the client

        Returns:
            {"token": String}: the clients auth token
        """
        return {"token": str.encode(self.token), "version": 1}

    Auth.responder(auth)


class COMPClientFactory(ClientFactory):
    """factory for COMP clients"""

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """builds the COMP protocol"""
        return COMPClientProtocol(
            agent=None, token="ThisIsSomeCoolDummyToken"
        )  # TODO: there is something fucked up with the agent...
