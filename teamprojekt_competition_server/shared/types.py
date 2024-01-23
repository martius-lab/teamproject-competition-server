"""contains types used by the server and the client"""

from typing import TypeAlias
import uuid

# NOTE: conda doesn't support python 3.12 (21.01.24)
#       that's why we cannot use the type keyword

PlayerID: TypeAlias = uuid.UUID
GameID: TypeAlias = uuid.UUID
