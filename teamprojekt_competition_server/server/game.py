"""base class for games"""

class Game:
    """game interface"""

    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2
        self.env = None

    async def start_game(self):
        """starts the game"""
        player1_ready = self.player1.start_game(self)
        player2_ready = self.player2.start_game(self)
        print(player1_ready, player2_ready)
        if player1_ready and player2_ready:
            await self.one_game_cycle()
        elif(player2_ready):
            self.end_game("Player 1 is not ready")
        else:
            self.end_game("Player 2 is not ready")
            
        
    async def one_game_cycle(self):
        """sends a step request to both players and changes the enviroment accordingly."""
        # has to be implemented in a subclass
        pass

    def get_action(self, player):
        """request an valid action from one player"""
        for _ in range(3): # each plyer gets three tries for a valid move
            action = player.step(env=self.env)
            if self.valid_action(action): return action
        self.end_game("Invalid action")
        return None

    def valid_action(self, action):
        """check weather an action is valid"""
        return True

    def check_game_finished(self) -> bool:
        """detirmens if the game has ended

        Returns:
            bool: returns true if game has ended
        """
        return True

    def end_game(self, reason = "unknown"):
        """ends the game"""
        print("Game has endet. Reason: " + reason) #log the reason the game has endet
        self.player1.end_game()
        self.player2.end_game()
        

    def receive_step(self, action):
        """handles step received from player

        Args:
            action (int): players requested action."""

        print(f"Game: Player {self.current_player} made the step {action}.")
        self.current_player = 1 if self.current_player == 2 else 2
        if input("End game? (y/n)") == "y":
            self.end_game()
        else:
            self.send_step()

class AlternatingGame(Game):
    """Game class where the environment is updated BETWEEN each players step"""
    async def one_game_cycle(self):
        """sends a step request to both players and changes the enviroment accordingly."""
        #step for player1
        action1 = self.get_action(player=self.player1)
        if action1==None: return # exit if move wasn't valid
        self.update_environment(action1)
        if (self.check_game_finished): # check if game has endet
            return

        #step for player2
        action2 = self.get_action(player=self.player1)
        if action1==None: return # exit if move wasn't valid
        self.update_environment(action2)
        if (self.check_game_finished): # check if game has endet
            return
        
        await self.one_game_cycle
    
    def update_environment(self, action):
        """update the game enviroment after one action"""
        pass

class SimultaneousGame(Game):
    """Game class where the environment is AFTER both players made a step"""
    async def one_game_cycle(self):
        """sends a step request to both players and changes the enviroment accordingly."""
        #step for player1
        action1 = self.get_action(player=self.player1)
        if action1==None: return # exit if move wasn't valid
        #step for player2
        action2 = self.get_action(player=self.player1)
        if action2==None: return # exit if move wasn't valid
        #update enviroment
        self.update_environment(action1=action1, action2=action2)
        
        if (not self.check_game_finished): # check if game has endet
            await self.one_game_cycle
        else:
            return
    
    def update_environment(self, action1, action2):
        """update the game enviroment after both actions"""
        pass