"""base class for agent"""
from typing import final
from client import COMPClient


class COMPAgent:
    """agent interface"""

    def __init__(self) -> None:
        self.client = COMPClient(agent=self)
        pass

    def step(self, env):
        """this is an abstract method for one step that the
        agent makes and should be overwritten

        Args:
            env (_type_): current enviroment

        Raises:
            NotImplementedError: this method should be overwritten
        """
        raise NotImplementedError()

    @final
    def run(self, token: str):
        """connects and authenticate the agent over the client with the server

        Args:
            token (String): Token to verify the client
        """
        self.client.connect_client(token=token)
