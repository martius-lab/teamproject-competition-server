from twisted.internet import defer, reactor, protocol
from twisted.internet.task import deferLater
from twisted.protocols import amp
from twisted.protocols.amp import Integer, String, Boolean, Command, AmpList
from typing import final
from client import COMPClient


class COMPAgent:
    def __init__(self) -> None:
        self.client = COMPClient(self.step)
        pass

    def step(self, env):
        pass

    @final
    def run(self, token):
        self.client.connect_client(token=token)
