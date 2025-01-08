import random
from comprl.client import Agent, launch_client


class MyAgent(Agent):
    """An agent for the simple game."""

    def get_step(self, obv: list[float]):
        return [float(input("enter number: ")) or float(random.randint(1, 2))]

    def on_start_game(self, game_id: int):
        print("game started")

    def on_end_game(self, result, stats):
        print("game ended")


if __name__ == "__main__":
    launch_client(lambda args: MyAgent())
