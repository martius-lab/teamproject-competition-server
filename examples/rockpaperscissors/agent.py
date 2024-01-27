from comprl.client.agent import COMPAgent


class RPSAgent(COMPAgent):
    """Dummy Agent for testing. Returns random action"""

    def step(self, obv: list[float]) -> list[float]:
        """exampel step function with human interaction"""
        user_input = float(input("Enter a number between 0 and 2: "))
        while user_input < 0 or user_input > 2:
            print("Invalid input. Please enter a number between 0 and 2.")
            user_input = float(input("Enter a number between 0 and 2: "))
        return [user_input]


bob = RPSAgent()
bob.run("ExampleToken")
