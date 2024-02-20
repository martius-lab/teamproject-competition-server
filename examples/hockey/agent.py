import numpy as np
from comprl.client.agent import COMPAgent

import laserhockey.hockey_env as h_env


class Weak_Hockey_Agent(COMPAgent):
    """Weak opponent agent from hockey game"""

    def __init__(self) -> None:
        self.agent = h_env.BasicOpponent()  # initialize agent
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
        self.agent = h_env.BasicOpponent(weak=False)  # initialize agent
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


bob = Weak_Hockey_Agent()
bob.run("ExampleToken")
