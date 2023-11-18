class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def get_board(self):
        return self.board
    
    def get_current_player(self):
        return self.current_player
    
    def set_current_player(self, player):
        self.current_player = player

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))

    def check_winner(self):
        # rows and columns
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)) or \
               all(self.board[j][i] == self.current_player for j in range(3)):
                return True
        # diagonals
        if all(self.board[i][i] == self.current_player for i in range(3)) or \
           all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def play_one_step(self, row, col):
        #print(f"It's player {self.current_player}'s turn.")
        #row = int(input("Enter the row (0, 1, or 2): ")) 
        #col = int(input("Enter the column (0, 1, or 2): "))
            
        if row<=-1 or row >=3 or col<=-1 or col >=3:
            return []
            #print("No valid input. Try again.")
            
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
        else:
            return []
            #print("Cell already occupied. Try again.")
        

        if self.check_winner():
            self.print_board()
            #print(f"Player {self.current_player} wins!")
            return ['win']

        if self.is_board_full():
            self.print_board()
            #print("The board is full. It's a tie!")
            return ['full']
        
        #self.print_board()