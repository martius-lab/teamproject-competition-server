from typing import Optional
from twisted.internet.interfaces import IAddress
from twisted.protocols import amp
from twisted.internet.protocol import Protocol, ServerFactory
import sys
sys.path.insert(0, '')
from teamprojekt_competition_server.shared.commands import AuthClient, StartGame, EndGame, Step

class COMPServerProtocol(amp.AMP):
    
    def auth_client(self, token, version):
        print (f'--- Authentification --- \nToken: {token} | Version: {version}')
        self.callRemote(StartGame, game_id=222).addCallback(lambda x : (print(x), self.step()))
        return {'uuid': 1111} #dummy uuid
    AuthClient.responder(auth_client)
    
    def step(self):
        def next_step(x):
            print(x)
            print('next step? (y/n)')
            if input() == 'y' : 
                self.step()
            else:
                self.endGame()
        self.callRemote(Step, env=1).addCallback(next_step)
    
    def endGame(self):
        self.callRemote(EndGame, result=True, stats=4).addCallback(lambda x : print(x))

    

class COMPServerFactory(ServerFactory):
    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        return COMPServerProtocol()