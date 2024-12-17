import random
from comprl.client import Agent, launch_client


class MyAgent(Agent):
    """An Rock-Paper-Scissor agent."""

    def get_step(self, obv: list[float]):
        return [float(random.randint(0, 2))]

    def on_start_game(self, game_id: int):
        print("game started")

    def on_end_game(self, result, stats):
        text_result = "won" if result else "lost"
        print(
            f"game ended: {text_result} with my score: "
            f"{stats[0]} against the opponent with score: {stats[1]}"
        )


if __name__ == "__main__":
    launch_client(lambda args: MyAgent())
