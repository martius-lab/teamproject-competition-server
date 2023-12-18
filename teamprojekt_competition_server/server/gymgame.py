"""Game using gym"""

import gymnasium as gym
import logging as log

import random


from .interfaces import IGame, IPlayer


class GymGame(IGame):
    """game class with the game logic being a gym env"""

    def __init__(self, players: list[IPlayer], env_name: str = "Pendulum-v1") -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handeld by the abstarct class
            env_name (str, optional): Name of the used gym env. Defaults to
                                      "Pendulum-v1" for testing purposes.
                                      The default might change later.
        """
        self.env = gym.make(
            env_name, render_mode="human"
        )  # add ', render_mode="human" ' to render the env.

        # initialize terminated and truncated, so the game hasn't endet by default.
        self.terminated = False
        self.truncated = False
        self.cycle_count = 0
        self.MAX_CYCLE_COUNT = 1000

        self.observation, self.info = self.env.reset()

        log.debug("created a new gym env")

        super().__init__(players)

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """
        return super().start()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended.
                                    Defaults to "unknown"
        """
        self.env.close()
        return super().end(reason)

    def _update_enviroment(self):
        """perform one gym step, using the actions collected by _game_cycle"""
        (
            self.observation,
            self.reward,
            self.terminated,
            self.truncated,
            self.info,
        ) = self.env.step(
            self.current_actions[random.randint(0, 1)]
        )  # TODO remove random. This is only for testing purposes
        self.cycle_count += 1
        if self.cycle_count > self.MAX_CYCLE_COUNT:
            self.terminated = True

    def _game_cycle(self):
        return super()._game_cycle()

    def _validate_action(self, action) -> bool:
        return self.env.action_space.contains(
            action
        )  # check if the action is in the action space and thus valid

    def _is_finished(self) -> bool:
        return self.terminated or self.truncated

    def _observation(self):
        return self.observation.tolist()  # obs is an np array, we need list

    def _player_won(self, index) -> bool:
        return False  # TODO find the winner

    def _player_stats(self, index) -> int:
        return 0  # TODO
