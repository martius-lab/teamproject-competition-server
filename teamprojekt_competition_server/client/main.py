from agent import COMPAgent

if __name__ == "__main__":

    class MyAgent(COMPAgent):
        def step(self, env):
            return int(input(f"Enviroment: {env} \nEnter a move: "))

    agent = MyAgent()
    token = b"ABC"  # dummy token
    agent.run(token)
