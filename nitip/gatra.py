import random

class Game:
    def __init__(self):
        self.grid = ['P', 'E']  # P is player, E is enemy
        self.player_points = 0
        self.enemy_points = 0
        self.enemy_actions = 'GGGMGMGGMM'  # predefined actions for enemy
        self.turn = 0
        self.enemy_turn_index = 0
        self.sequence = ""
        self.enemy_sequence = ""  # To store enemy's actions

    def input_move(self, msg, valid_actions):
        move = input(msg).strip().upper()
        while move not in valid_actions:
            move = input(f"Invalid input. Please enter one of {valid_actions}: ").strip().upper()
        return move

    def get_enemy_action(self):
        action = self.enemy_actions[self.enemy_turn_index]
        if action == 'M':
            return 'M'  # Enemy must move
        elif action == 'G':
            return random.choice(['W', 'P', 'G'])  # Enemy can choose randomly
        return action

    def calculate_points(self, player_action, enemy_action):
        if player_action == 'W':
            self.player_points += 3
            self.enemy_points -= 4
        elif player_action == 'P':
            self.player_points -= 3
            self.enemy_points += 3
        elif player_action == 'G':
            self.player_points += 1
        elif player_action == 'M':
            self.player_points -= 1

        if enemy_action == 'W':
            self.player_points -= 4
            self.enemy_points += 3
        elif enemy_action == 'P':
            self.player_points += 3
            self.enemy_points -= 3
        elif enemy_action == 'G':
            self.enemy_points += 0
        elif enemy_action == 'M':
            self.enemy_points += 0

    def play(self):
        print("Welcome to the Game!")
        while self.turn < 10:
            print(f"\nTurn {self.turn + 1}")
            if self.grid[1] == 'E':  # If enemy is present
                player_action = self.input_move("There is an enemy, input move (W/P/G/M): ", ['W', 'P', 'G', 'M'])
            else:  # No enemy
                player_action = self.input_move("There is no one here, input move (G/M): ", ['G', 'M'])

            # Execute player action
            if player_action == 'M':
                self.grid[0] = ' '  # Player moves away
                self.grid[1] = ' '  # The enemy is removed from the grid
            elif player_action == 'S':
                pass  # Stay

            self.sequence += player_action

            # Get enemy action
            enemy_action = self.get_enemy_action()
            self.enemy_sequence += enemy_action  # Track enemy's action
            print(f"Enemy action: {enemy_action}")

            # Calculate points
            self.calculate_points(player_action, enemy_action)

            # Check if player and enemy are on the same grid
            if player_action != 'M':
                self.grid[1] = 'E'  # Enemy is present if player did not move away

            # Move enemy if needed
            if enemy_action == 'M' and self.grid[1] == 'E':
                self.grid[1] = ' '  # Enemy moves away
                self.grid[0] = 'E'  # Move enemy to player position if applicable

            self.turn += 1
            self.enemy_turn_index += 1

        # Game ends
        print(f"\nYour sequence is {self.sequence}, Enemy's sequence is {self.enemy_sequence}, points are (Player: {self.player_points}, Enemy: {self.enemy_points})")

if __name__ == "__main__":
    game = Game()
    game.play()
