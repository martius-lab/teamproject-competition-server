from agent import COMPAgent

if __name__ == '__main__':
    class MyAgent(COMPAgent):
        def step(env):
            return env
    agent = MyAgent()
    token = b"ABC" #dummy token
    agent.run(token)