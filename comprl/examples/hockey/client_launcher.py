"""Example client script.

Basic example on how to implement a client script.
It implements an Agent that wraps around a learned policy imported from the hockey
package.
"""

import argparse

from comprl.client import Agent, launch_client

import hockey.hockey_env as h_env
import numpy as np


class RandomAgent(Agent):
    """A hockey agent that simply uses random actions."""

    def get_step(self, obv: list[float]):
        return np.random.uniform(-1, 1, 4).tolist()

    def on_start_game(self, game_id: int):
        print("game started")

    def on_end_game(self, result, stats):
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

    def get_step(self, obv: list[float]):
        return self.hockey_agent.act(obv).tolist()

    def on_start_game(self, game_id: int):
        print("game started")

    def on_end_game(self, result, stats):
        text_result = "won" if result else "lost"
        print(
            f"game ended: {text_result} with my score: "
            f"{stats[0]} against the opponent with score: {stats[1]}"
        )


# Function to initialize the agent.  This function is used with `launch_client` below,
# to lauch the client and connect to the server.
def initialize_agent(agent_args: list[str]) -> Agent:
    # Use argparse to parse the arguments given in `agent_args`.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--agent",
        type=str,
        choices=["weak", "strong", "random"],
        default="weak",
        help="Which agent to use.",
    )
    args = parser.parse_args(agent_args)

    # Initialize the agent based on the arguments.
    agent: Agent
    if args.agent == "weak":
        agent = HockeyAgent(weak=True)
    elif args.agent == "strong":
        agent = HockeyAgent(weak=False)
    elif args.agent == "random":
        agent = RandomAgent()
    else:
        raise ValueError(f"Unknown agent: {args.agent}")

    # And finally return the agent.
    return agent


if __name__ == "__main__":
    launch_client(initialize_agent)
