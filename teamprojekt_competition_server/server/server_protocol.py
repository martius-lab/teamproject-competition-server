from typing import Optional
from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import Protocol, ServerFactory
from teamprojekt_competition_server.shared.commands import AuthClient, StartGame, EndGame, Step

class COMPServerProtocol(amp.AMP):
    
    def auth_client(self, token, version):
        print (f'--- Authentification --- \nToken: {token} | Version: {version}')
        self.callRemote(StartGame, game_id=222).addCallback(lambda x : print(x))
        return {'uuid': 1111} #dummy uuid
    AuthClient.responder(auth_client)
    
    
class COMPServerFactory(ServerFactory):
    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        return COMPServerProtocol()