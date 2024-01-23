'''Several examples for agents for different games'''
from .agent import COMPAgent

import laserhockey.hockey_env as h_env
import numpy as np
import random

class Weak_Hockey_Agent(COMPAgent):
    """Weak opponent agent from hockey game"""
    def __init__(self) -> None:
        self.agent = h_env.BasicOpponent() # initialize agent
        super().__init__()

    def step(self, obv: list[float]) -> list[float]:
        """step function

        Args:
            obv (list[float]): observation

        Returns:
            list(float): action
        """

        return self.agent.act(obv)

class Strong_Hockey_Agent(COMPAgent):
    """Strong opponent agent from hockey game"""
    def __init__(self) -> None:
        self.agent = h_env.BasicOpponent(weak=False) # initialize agent
        super().__init__()

    def step(self, obv: list[float]) -> list[float]:
        """step function

        Args:
            obv (list[float]): observation

        Returns:
            list(float): action
        """

        return self.agent.act(obv)

class Random_Hockey_Agent(COMPAgent):
    """Dummy Agent for testing. Returns random action"""

    def step(self, obv: list[float]) -> list[float]:
        """dummy step function

        Args:
            obv (list[float]): observation

        Returns:
            list(float): action
        """

        return np.random.uniform(-1, 1, 4).tolist()
        # Action Space Box(-1.0, 1.0, (4,), float32)

class Rock_Paper_Scissors_Agent(COMPAgent):
    """Dummy Agent for testing. Returns random action"""

    def step(self, obv: list[float]) -> list[float]:
        """dummy step function

        Args:
            obv (list[float]): observation

        Returns:
            list(float): action
        """
        # return float(input(f"Observation: {obv} | Enter a move: "))
        print(random.choice([0.0, 1.0, 2.0]))
        return [random.choice([0.0, 1.0, 2.0])]
        # Action Space Box(-2.0, 2.0, (1,), float32)