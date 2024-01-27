from comprl.client.agent import COMPAgent


class ExampleAgent(COMPAgent):
    """Dummy Agent for testing. Returns random action"""

    def step(self, obv: list[float]) -> list[float]:
        """exampel step function with human interaction"""
        return [input("enter action: ")]


bob = ExampleAgent()
bob.run("ExampleToken")
