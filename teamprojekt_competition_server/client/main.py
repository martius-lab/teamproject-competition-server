"""main class with dummy agend for testing"""
from .agent import COMPAgent

import random

# run with "python -m teamprojekt_competition_server.client.main"

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, obv):
            """dummy step function

            Args:
                obv (int): enviroment

            Returns:
                float: action
            """
            # return float(input(f"Observation: {obv} | Enter a move: "))
            return random.uniform(-1, 1)

    agent = MyAgent()
    agent.run("HelloWorldToken")
