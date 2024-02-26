from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import PlayerID

import laserhockey.hockey_env as h_env
import numpy as np


class HockeyGame(IGame):
    """game class with the game logic being the laser-hockey env"""

    def __init__(self, players: list[IPlayer]) -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handled by the abstract class
        """

        self.env = h_env.HockeyEnv()
        self.player_1_id = players[0].id
        self.player_2_id = players[1].id

        # number of rounds played per game and current score
        self.remaining_rounds: int = 4
        # Bool weather players play in default orientation or sides are swapped.
        # Alternates between rounds.
        self.sides_swapped = False

        # initialize terminated and truncated, so the game hasn't ended by default.
        self.terminated = False
        self.truncated = False

        # Bool if all rounds are finished
        self.finished = False
        print("Game created")

        super().__init__(players)

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """

        self.obs_player_left, self.info = self.env.reset()
        return super().start()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended.
                                    Defaults to "unknown"
        """
        self.env.close()
        return super().end(reason)

    def update(self, actions_dict: dict[PlayerID, list[float]]) -> bool:
        """perform one gym step, using the actions

        Returns:
            bool: True if the game is over, False otherwise.
        """
        self.env.render(mode="human")  # (un)comment to render or not

        if self.sides_swapped:  # change order of actions if sides are changed
            self.raw_actions = [
                actions_dict[self.player_2_id],
                actions_dict[self.player_1_id],
            ]

        else:
            self.raw_actions = [
                actions_dict[self.player_1_id],
                actions_dict[self.player_2_id],
            ]
        self.action = np.hstack(self.raw_actions)
        (
            self.obs_player_left,
            self.reward,
            self.terminated,
            self.truncated,
            self.info,
        ) = self.env.step(self.action)

        # check if current round has ended
        if self.terminated or self.truncated:
            # update score
            self.winner = self.info["winner"]
            if self.winner == 1:
                if self.sides_swapped:
                    self.scores[self.player_2_id] = self.scores[self.player_2_id] + 1
                else:
                    self.scores[self.player_1_id] = self.scores[self.player_1_id] + 1
            if self.winner == -1:
                if self.sides_swapped:
                    self.scores[self.player_1_id] = self.scores[self.player_1_id] + 1
                else:
                    self.scores[self.player_2_id] = self.scores[self.player_2_id] + 1

            # reset env, swap player side and decrease remaining rounds
            self.obs_player_left, self.info = self.env.reset()
            self.sides_swapped = not self.sides_swapped
            self.remaining_rounds = self.remaining_rounds - 1

            # check if it was the last round
            if self.remaining_rounds == 0:
                self.finished = True

        return self.finished

    def _validate_action(self, action) -> bool:
        """check if the action is in the action space of the env"""
        # can't use self.env.action_space.contains as tis is a action of one player
        # and the action space is for both players. So I basically copied the code from
        # the contains() function.
        action = np.array(action)
        return bool(
            action.shape == (4,) and np.all(action >= -1) and np.all(action <= 1)
        )
        # check if the action is in the action space and thus valid

    def get_observation(self, id: PlayerID) -> list[float]:
        """return the correct obs respecting if sides are swapped

        Args: id: PlayerID of the player to get the observation for

        Returns: list[float]: observation of the player with the given id"""
        if (id == self.player_2_id) and (not self.sides_swapped):
            return self.env.obs_agent_two().tolist()  # obs is an np array, we need list
        elif (id == self.player_1_id) and self.sides_swapped:
            return self.env.obs_agent_two().tolist()  # obs is an np array, we need list
        else:
            return self.obs_player_left.tolist()  # obs is an np array, we need list

    def _player_won(self, id: PlayerID) -> bool:
        """check if a player has won the game

        Args: id: PlayerID of the player to check

        Returns: bool: True if the player has won, False otherwise"""
        if not self.finished:  # if game hasn't ended nobody has won
            return False

        # determine winner using score
        if id == self.player_1_id:
            return self.scores[self.player_1_id] > self.scores[self.player_2_id]
        if id == self.player_2_id:
            return self.scores[self.player_2_id] > self.scores[self.player_1_id]
        return False

    def get_player_result(self, id: PlayerID) -> int:
        """get the score of a player
        Args: id: PlayerID of the player to get the score of
        Returns: int: score of the player with the given id"""
        return int(self.scores[id])
