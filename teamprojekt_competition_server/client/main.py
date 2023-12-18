"""main class with dummy agend for testing"""
from .agent import COMPAgent

import random

# run with "python -m teamprojekt_competition_server.client.main"

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, obv: list[float]) -> list[float]:
            """dummy step function

            Args:
                obv (list(float)): enviroment

            Returns:
                list(float): action
            """
            # return float(input(f"Observation: {obv} | Enter a move: "))
            return [random.uniform(-2, 2)]  # Action Space Box(-2.0, 2.0, (1,), float32)

    agent = MyAgent()
    agent.run("HelloWorldToken")
