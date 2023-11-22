"""main class with dummy agend for testing"""
from .agent import COMPAgent

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        """Dummy Agent for testing"""

        def step(self, env):
            """dummy step function

            Args:
                env (int): enviroment

            Returns:
                int: action
            """
            return int(input(f"Enviroment: {env} \nEnter a move: "))

    agent = MyAgent()
    token = "ABC"  # dummy token
    agent.run(token)
    print("Hello")
