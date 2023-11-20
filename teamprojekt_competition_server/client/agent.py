from typing import final
from client import COMPClient
from abc import ABC, abstractmethod


class COMPAgent:
    def __init__(self) -> None:
        self.client = COMPClient(agent=self)
        pass
    
    @abstractmethod
    def step(self, env):
        raise NotImplementedError()

    @final
    def run(self, token):
        self.client.connect_client(token=token)
