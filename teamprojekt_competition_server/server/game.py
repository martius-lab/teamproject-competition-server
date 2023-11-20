"""base class for games"""


class Game:
    """game interface"""

    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2
        self.current_player = 1
        self.env = 1
        self.num_ready = 0

    def send_step(self):
        """sends a step request to player instance."""
        player = self.player1 if (self.current_player == 1) else self.player2
        player.step(env=self.env)
        print(f"Game: Send Player {self.current_player} a step request.")

    def receive_step(self, action):
        """handles step received from player

        Args:
            action (int): players requested action."""

        print(f"Game: Player {self.current_player} made the step {action}.")
        self.current_player = 1 if self.current_player == 2 else 2
        if input("End game? (y/n)") == "y":
            self.player1.end_game()
            self.player2.end_game()
        else:
            self.send_step()

    def ready(self):
        """ "manages the counter for ready players"""
        print("Player is ready.")
        self.num_ready += 1
        if self.num_ready == 2:
            self.send_step()