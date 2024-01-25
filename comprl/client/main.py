"""main class with dummy agent for testing"""

from .example_agents import Strong_Hockey_Agent

import logging as log


log.basicConfig(level=log.DEBUG)

# run with "python -m comprl.client.main"

if __name__ == "__main__":
    agent = Strong_Hockey_Agent()
    agent.run("HelloWorldToken")
