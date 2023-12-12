from .interfaces import IPlayer

_connected_players : list[IPlayer] = []

def register_player(player : IPlayer):
    _connected_players.append(player)