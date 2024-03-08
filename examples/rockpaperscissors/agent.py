from comprl.client import Agent
import random


RPSAgent = Agent()


@RPSAgent.event
def get_step(obv: list[float]):
    return [float(random.randint(0, 2))]


@RPSAgent.event
def on_start_game(game_id: int):
    print("game started")


@RPSAgent.event
def on_end_game(result, stats):
    text_result = "won" if result else "lost"
    print(
        f"game ended: {text_result} with my score: "
        f"{stats[0]} against the opponent with score: {stats[1]}"
    )


RPSAgent.run("token" + str(input("enter 1, 2, 3 or 4 to choose token: ")))
