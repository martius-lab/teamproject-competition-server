"""
This is the game logic of a dummy game (TicTacToe).
"""


class TicTacToe:
    """
    This class represents a TicTacToe game.
    """

    def __init__(self):
        """The constructor creates an empty board and sets the player to 'X' by default."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def get_board(self):
        """getter for the board

        Returns:
            2D Array(String): current board
        """
        return self.board

    def get_current_player(self):
        """getter for the current player

        Returns:
            String: current player
        """
        return self.current_player

    def set_current_player(self, player):
        """setter for the current player

        Args:
            player (String):current player
        """
        self.current_player = player

    def print_board(self):
        """prints the board in the console"""
        for row in self.board:
            print(" | ".join(row))

    def check_winner(self):
        """checks if the current player has won the game

        Returns:
            Boolean: true if the current player has won, false otherwise
        """
        # rows and columns
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)) or all(
                self.board[j][i] == self.current_player for j in range(3)
            ):
                return True
        # diagonals
        if all(self.board[i][i] == self.current_player for i in range(3)) or all(
            self.board[i][2 - i] == self.current_player for i in range(3)
        ):
            return True
        return False

    def is_board_full(self):
        """checks if the board is full

        Returns:
            Boolean: true if the board is full, false otherwise
        """
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def play_one_step(self, row, col):
        """Executes one move in the game

        Args:
            row (int): The row in which the player wants to place his token next.
            col (int): The column in which the player wants to place his token next.

        Returns:
            Array(String): The board after the move.
            If the input was invalid or the field was already occupied, an empty array is returned.
            If the player has won, ['win'] is returned. If the board is full, ['full'] is returned.
        """
        # print(f"It's player {self.current_player}'s turn.")
        # row = int(input("Enter the row (0, 1, or 2): "))
        # col = int(input("Enter the column (0, 1, or 2): "))

        if row <= -1 or row >= 3 or col <= -1 or col >= 3:
            return []
            # print("No valid input. Try again.")

        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
        else:
            return []
            # print("Cell already occupied. Try again.")

        if self.check_winner():
            self.print_board()
            # print(f"Player {self.current_player} wins!")
            return ["win"]

        if self.is_board_full():
            self.print_board()
            # print("The board is full. It's a tie!")
            return ["full"]

        return self.board

        # self.print_board()
