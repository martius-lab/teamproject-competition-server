import numpy as np
from comprl.client import Agent

Random_Hockey_Agent = Agent()


@Random_Hockey_Agent.event
def get_step(obv: list[float]):
    return np.random.uniform(-1, 1, 4).tolist()


@Random_Hockey_Agent.event
def on_start_game(game_id: int):
    print("game started")


@Random_Hockey_Agent.event
def on_end_game(result, stats):
    print("game ended")


Random_Hockey_Agent.run(
    ["HelloWorld", "HelloMoon"][int(input("enter 0 or 1 to choose token: "))]
)
