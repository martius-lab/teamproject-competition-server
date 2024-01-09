"""main class with dummy agent for testing"""
import logging as log
import numpy as np

from .agent import COMPAgent
import random

log.basicConfig(level=log.DEBUG)


# run with "python -m teamprojekt_competition_server.client.main"

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, obv: list[float]) -> list[float]:
            """dummy step function

            Args:
                obv (list[float]): observation

            Returns:
                list(float): action
            """
            
            return np.random.uniform(-1,1,3)  # Action Space Box(-1.0, 1.0, (3,), float32)

    class Rock_Paper_Scissors_Agent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, obv: list[float]) -> list[float]:
            """dummy step function

            Args:
                obv (list[float]): environment

            Returns:
                list(float): action
            """
            # return float(input(f"Observation: {obv} | Enter a move: "))
            print(random.choice([0.0, 1.0, 2.0]))
            return [random.choice([0.0, 1.0, 2.0])]
            # Action Space Box(-2.0, 2.0, (1,), float32)

    agent = MyAgent() #Rock_Paper_Scissors_Agent()
    agent.run("HelloWorldToken")
