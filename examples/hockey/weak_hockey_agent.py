from comprl.client import Agent

import laserhockey.hockey_env as h_env

Weak_Hockey_Agent = Agent()
agent = h_env.BasicOpponent()  # initialize agent


@Weak_Hockey_Agent.event
def get_step(obv: list[float]):
    return agent.act(obv).tolist()


@Weak_Hockey_Agent.event
def on_start_game(game_id: int):
    print("game started")


@Weak_Hockey_Agent.event
def on_end_game(result, stats):
    print("game ended")


Weak_Hockey_Agent.run("token" + str(input("enter 1, 2, 3 or 4 to choose token: ")))
