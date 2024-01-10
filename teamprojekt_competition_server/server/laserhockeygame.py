"""Game using the laser-hockey env from https://github.com/martius-lab/laser-hockey-env.git"""

import logging as log
import numpy as np
import laserhockey.laser_hockey_env as lh
import gymnasium as gym
from importlib import reload


from .interfaces import IGame, IPlayer


class LaserHockeyGame(IGame):
    """game class with the game logic being the laser-hockey env"""

    def __init__(
        self, players: list[IPlayer], env_name: str = "laser_hockey_env"
    ) -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handled by the abstract class
            env_name (str, optional): Name of the used gym env. Defaults to
                                      "Pendulum-v1" for testing purposes.
                                      The default might change later.
        """
        if (
            env_name == "laser_hockey_env"
        ):  # not pretty, but I don't want to register the env at the moment
            reload(lh)
            self.env = lh.LaserHockeyEnv()
        else:
            self.env = gym.make(
                env_name, render_mode="human"
            )  # add ', render_mode="human" ' to render the env.

        # initialize terminated and truncated, so the game hasn't ended by default.
        self.terminated = False
        self.truncated = False
        # TODO use the build in function from gym to limit the amount of steps

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
