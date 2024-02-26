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
    text_result = "won" if result else "lost"
    print(
        f"game ended: {text_result} with my score {stats[0]} and other score {stats[1]}"
    )


Weak_Hockey_Agent.run(
    ["HelloWorld", "HelloMoon"][int(input("enter 0 or 1 to choose token: "))]
)
