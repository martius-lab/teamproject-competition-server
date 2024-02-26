from comprl.client import Agent

import laserhockey.hockey_env as h_env

Strong_Hockey_Agent = Agent()
agent = h_env.BasicOpponent(weak=False)  # initialize agent


@Strong_Hockey_Agent.event
def get_step(obv: list[float]):
    return agent.act(obv).tolist()


@Strong_Hockey_Agent.event
def on_start_game(game_id: int):
    print("game started")


@Strong_Hockey_Agent.event
def on_end_game(result, stats):
    print("game ended")


Strong_Hockey_Agent.run("token" + str(input("enter 1, 2, 3 or 4 to choose token: ")))
