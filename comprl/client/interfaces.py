"""
This module contains the interface for the agent.
"""


class IAgent:
    """agent interface which could be used by the end-user"""

    def run(self, token: str):
        """
        Runs the agent with the specified token.

        Args:
            token (str): The token used for authentication.
        """
        self.token = token

    def auth(self) -> str:
        """
        Returns the authentication token.

        Returns:
            str: The authentication token.
        """
        return self.token

    def on_start_game(self, game_id: int):
        """
        Called when a new game starts.

        Args:
            game_id (int): The ID of the new game.

        Returns:
            bool: True if the agent is ready to play, False otherwise.
        """
        return True

    def get_step(self, obv: list[float]) -> list[float]:
        """
        Requests the agent's action based on the current observation.

        Args:
            obv (list[float]): The current observation.

        Returns:
            list[float]: The agent's action.
        """
        raise NotImplementedError("step function not implemented")

    def on_end_game(self, result, stats) -> bool:
        """
        Called when a game ends.

        Args:
            result: The result of the game.
            stats: The statistics of the game.

        Returns:
            bool: True if the agent handled the end of the game, False otherwise.
        """
        return True

    def on_error(self, msg):
        """
        Called when an error occurs.

        Args:
            msg: The error message.
        """
        pass
