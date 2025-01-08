"""Example agents for the hockey game."""

from __future__ import annotations

import hockey.hockey_env as h_env
import numpy as np

from comprl.client import Agent


class RandomAgent(Agent):
    """A hockey agent that simply uses random actions."""

    def get_step(self, obv: list[float]) -> list[float]:
        return np.random.uniform(-1, 1, 4).tolist()

    def on_start_game(self, game_id: int):
        print("game started")

    def on_end_game(self, result: bool, stats: list[float]) -> None:
        text_result = "won" if result else "lost"
        print(
            f"game ended: {text_result} with my score: "
            f"{stats[0]} against the opponent with score: {stats[1]}"
        )


class HockeyAgent(Agent):
    """A hockey agent that can be weak or strong."""

    def __init__(self, weak: bool) -> None:
        super().__init__()

        self.hockey_agent = h_env.BasicOpponent(weak=weak)

    def get_step(self, obv: list[float]) -> list[float]:
        return self.hockey_agent.act(obv).tolist()

    def on_start_game(self, game_id: int) -> None:
        print("game started")

    def on_end_game(self, result: bool, stats: list[float]) -> None:
        text_result = "won" if result else "lost"
        print(
            f"game ended: {text_result} with my score: "
            f"{stats[0]} against the opponent with score: {stats[1]}"
        )
