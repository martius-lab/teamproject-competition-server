"""Game using the laser-hockey env from https://github.com/martius-lab/laser-hockey-env.git"""

import logging as log
import numpy as np
import laserhockey.laser_hockey_env as lh

# import gymnasium as gym
from importlib import reload


from .interfaces import IGame, IPlayer


class LaserHockeyGame(IGame):
    """game class with the game logic being the laser-hockey env"""

    def __init__(self, players: list[IPlayer]) -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handled by the abstract class
        """

        reload(lh)
        self.env = lh.LaserHockeyEnv()

        # initialize terminated and truncated, so the game hasn't ended by default.
        self.terminated = False
        self.truncated = False
        # TODO use the build in function from gym to limit the amount of steps

        log.debug("created a new gym env")

        super().__init__(players)

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """

        self.observation, self.info = self.env.reset()
        return super().start()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended.
                                    Defaults to "unknown"
        """
        self.env.close()
        return super().end(reason)

    def _update_environment(self):
        """perform one gym step, using the actions collected by _game_cycle"""
        self.env.render()  # (un)comment to render or not
        (
            self.observation,
            self.reward,
            self.terminated,
            self.truncated,
            self.info,
        ) = self.env.step(np.hstack(self.current_actions))

    def _validate_action(self, action) -> bool:
        return self.env.action_space.contains(
            action
        )  # check if the action is in the action space and thus valid

    def _is_finished(self) -> bool:
        return self.terminated or self.truncated

    def _observation(self, index):
        if index == 1:
            return self.env.obs_agent_two().tolist()  # obs is an np array, we need list
        else:
            return self.observation.tolist()  # obs is an np array, we need list

    def _player_won(self, index) -> bool:
        self.winner = self.info["winner"]
        if self.winner == 0:  # draw
            return False
        if index == 0:
            return self.winner == 1  # check if left player won
        if index == 1:
            return self.winner == -1  # check if right player won
        return False

    def _player_stats(self, index) -> int:
        return 0  # TODO where tf is th score stored?
