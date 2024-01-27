import numpy as np
from comprl.server import player_manager
from comprl.server.game_result import GameEndState, GameResult
from comprl.server.interfaces import IGame, IPlayer

import laserhockey.hockey_env as h_env

from comprl.server.server import COMPServer


class HockeyGame(IGame):
    """game class with the game logic being the laser-hockey env"""

    def __init__(self, players: list[IPlayer]) -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handled by the abstract class
        """

        self.env = h_env.HockeyEnv()

        # number of rounds played per game and current score
        self.remaining_rounds: int = 4
        self.score = [0, 0]
        # Bool weather players play in default orientation or sides are swapped.
        # Alternates between rounds.
        self.sides_swapped = False

        # initialize terminated and truncated, so the game hasn't ended by default.
        self.terminated = False
        self.truncated = False

        # Bool if all rounds are finished
        self.finished = False

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

    def _update_environment(self):
        """perform one gym step, using the actions collected by _game_cycle"""
        self.env.render(mode="human")  # (un)comment to render or not

        if self.sides_swapped:  # change order of actions if sides are changed
            self.action = np.hstack(np.flip(self.current_actions, 0))
        else:
            self.action = np.hstack(self.current_actions)
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
                    self.score[1] = self.score[1] + 1
                else:
                    self.score[0] = self.score[0] + 1
            if self.winner == -1:
                if self.sides_swapped:
                    self.score[0] = self.score[0] + 1
                else:
                    self.score[1] = self.score[1] + 1

            # reset env, swap player side and decrease remaining rounds
            self.obs_player_left, self.info = self.env.reset()
            self.sides_swapped = not self.sides_swapped
            self.remaining_rounds = self.remaining_rounds - 1

            # check if it was the last round
            if self.remaining_rounds == 0:
                self.finished = True

    def _validate_action(self, action) -> bool:
        return self.env.action_space.contains(
            action
        )  # check if the action is in the action space and thus valid

    def _is_finished(self) -> bool:
        # check if no round needs to be played and last round has ended.
        return self.finished

    def _observation(self, index):
        # return the correct obs respecting if sides are swapped
        if (index == 1) and (not self.sides_swapped):
            return self.env.obs_agent_two().tolist()  # obs is an np array, we need list
        elif (index == 0) and self.sides_swapped:
            return self.env.obs_agent_two().tolist()  # obs is an np array, we need list
        else:
            return self.obs_player_left.tolist()  # obs is an np array, we need list

    def _player_won(self, index) -> bool:
        if not self.finished:  # if game hasn't ended nobody has won
            return False

        # determine winner using score
        if index == 0:
            return self.score[0] > self.score[1]
        if index == 1:
            return self.score[1] > self.score[0]
        return False

    def _player_stats(self, index) -> int:
        return self.score[index]

    def get_results(self) -> GameResult:
        """get the results of the game

        Returns:
            GameResult: results and statistics of the game
        """
        end_state = GameEndState.WIN.value
        if self.score[0] == self.score[1]:
            end_state = GameEndState.DRAW.value

        return GameResult(
            game_id=self.id,
            user1_id=player_manager.get_user_id(self.players[0].id),
            user2_id=player_manager.get_user_id(self.players[1].id),
            score_user_1=self.score[0],
            score_user_2=self.score[1],
            end_state=end_state,
            is_user1_winner=self._player_won(0),
            start_time=self.start_time,
        )


server = COMPServer(HockeyGame)
server.start()
