"""
    this module contains the bot class and two bots for the hockey game
"""

import abc
import logging as log
import laserhockey.hockey_env as h_env

from comprl.server.interfaces import IAction, IPlayer


class bot(IPlayer):
    """A bot player running locally on the server"""

    def __init__(self) -> None:
        super().__init__()
        # put the token for the bot here:
        self.token = ""
        # TODO: The bot needs to know its user_id

    def authenticate(self, result_callback):
        """authenticates player

        Args:
            result_callback (Callable): callback
        """
        return result_callback(self.token)

    def is_ready(self, result_callback) -> bool:
        """checks if the player is ready to play

        Returns:
            bool: returns true if the player is ready to play
        """
        return result_callback(True)

    def notify_start(self, game_id):
        """notifies player that the game has started"""
        return

    def get_action(self, obv, result_callback) -> IAction:
        """gets an action from the player

        Args:
            obv (Any): observation
            result_callback (Callable): callback

        Returns:
            IAction: action
        """
        return result_callback(self._get_step(obv))

    @abc.abstractmethod
    def _get_step(self, obv):
        """gets the step from the bot

        Args:
            obv (_type_): observation

        Returns:
            step list[float]: the step to be performed
        """
        ...

    def notify_end(self, result, stats):
        """notifies player that the game has ended"""
        return

    def disconnect(self, reason: str):
        """disconnect the player"""
        log.debug(f"Bot was tried to disconnect for reason: {reason}")
        return

    def notify_error(self, error: str):
        """notifies the player of an error"""
        log.debug(f"Bot received error: {error}")
        return

    def notify_info(self, msg: str):
        """notifies the player of an information"""
        log.debug(f"Bot received info: {msg}")
        return


# TODO: maybe move these to examples


class Weak_Hockey_Bot(bot):
    """The weak hockey bot"""

    def __init__(self):
        self.token = "weak_bot"
        self.bot = h_env.BasicOpponent()  # initialize agent
        super().__init__()
        # TODO: This ist not at all good. Simply put the user_id of the bot registered
        # in the database here
        self.user_id = 151

    def _get_step(self, obv) -> IAction:
        """gets the step from the bot

        Args:
            obv (_type_): observation

        Returns:
            step list[float]: the step to be performed
        """
        return self.bot.act(obv).tolist()


class Strong_Hockey_Bot(bot):
    """The strong hockey bot"""

    def __init__(self):
        self.token = "strong_bot"
        self.bot = h_env.BasicOpponent(weak=False)  # initialize agent
        super().__init__()
        # TODO: This ist not at all good. Simply put the user_id of the bot registered
        # in the database here
        self.user_id = 152

    def _get_step(self, obv) -> IAction:
        """gets the step from the bot

        Args:
            obv (_type_): observation

        Returns:
            step list[float]: the step to be performed
        """
        return self.bot.act(obv).tolist()
