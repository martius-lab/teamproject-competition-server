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
        f"game ended: {text_result} with my score: "
        f"{stats[0]} against the opponent with score: {stats[1]}"
    )


Weak_Hockey_Agent.run("token" + str(input("enter 1, 2, 3 or 4 to choose token: ")))

# restarting the reactor is not easy. This might work:
# https://www.blog.pythonlibrary.org/2016/09/14/restarting-a-twisted-reactor/
