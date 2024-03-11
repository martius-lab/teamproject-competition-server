from comprl.client import Agent

from multiprocessing import Process
import laserhockey.hockey_env as h_env

class Hockey_Agent(Agent):
    def __init__(self, weak:bool ) -> None:
        self.agent = h_env.BasicOpponent(weak=weak)  # initialize agent
        super().__init__()
    def get_step(self, obv: list[float]) -> list[float]:
        return self.agent.act(obv).tolist()


def start_agent(weak: bool, token: str):
    agent = Hockey_Agent(weak)
    agent.run(token)

if __name__ == "__main__":
    offset = 0
    for weak in [True, False]:
        for i in range(10):
            for j in range(5):
                p = Process(target = start_agent, args = (weak, f"token{i+offset}"))
                p.start()
        offset = 10