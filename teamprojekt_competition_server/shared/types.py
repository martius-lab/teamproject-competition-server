import uuid

#NOTE: conda doesn't support python 3.12 (21.01.24) that's why we cannot use the type keyword 

class PlayerID(uuid.UUID):
    pass

class GameID(uuid.UUID):
    pass