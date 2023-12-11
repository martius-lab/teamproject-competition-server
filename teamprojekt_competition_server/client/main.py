"""main class with dummy agend for testing"""
from .agent import COMPAgent

# run with "python -m teamprojekt_competition_server.client.main"

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, obv):
            """dummy step function

            Args:
                obv (int): enviroment

            Returns:
                int: action
            """
            return int(input(f"Observation: {obv} | Enter a move: "))

    agent = MyAgent()
    agent.run("HelloWorldToken")
