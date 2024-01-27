"""main class with dummy agent for testing"""

from .example_agents import Strong_Hockey_Agent

import logging as log


log.basicConfig(level=log.DEBUG)

# run with "python -m comprl.client.main"

if __name__ == "__main__":
    token1 = "e3a0222f-2b8b-49e2-8305-7c5a3c9b48c6"
    token2 = "1a11abc1-774d-4582-9519-4ae28c5ae4d3"

    agent = Strong_Hockey_Agent()  # Rock_Paper_Scissors_Agent()
    agent.run(token1)
