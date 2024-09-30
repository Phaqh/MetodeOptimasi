import random

# Constants
POPULATION_SIZE = 100
GENOME_LENGTH = 10  # Length of action sequence
MUTATION_RATE = 0.1
GENERATIONS = 10

ACTIONS = ['W', 'P', 'G', 'M']
ENEMY_ACTIONS = 'GGGMGMGGMM'  # Penentuan actions enemy

class Game:
    def __init__(self, player_actions):
        self.player_points = 0
        self.enemy_points = 0
        self.turn = 0
        self.sequence = ""
        self.enemy_sequence = ""  # menyimpan enemy's actions
        self.player_actions = player_actions  # sequence action Player's
        self.enemy_war_once = False  # Track jika if enemy has used War

    def calculate_points(self, player_action, enemy_action):
        if player_action == 'W':
            self.player_points += 1
            self.enemy_points -= 5
        elif player_action == 'P':
            self.player_points -= 5
            self.enemy_points += 3
        elif player_action == 'G':
            self.player_points += 1
        elif player_action == 'M':
            self.player_points -= 1

        if enemy_action == 'W':
            self.player_points -= 5
            self.enemy_points += 1
        elif enemy_action == 'P':
            self.player_points += 3
            self.enemy_points -= 5
        elif enemy_action == 'G':
            self.enemy_points += 1
        elif enemy_action == 'M':
            self.enemy_points -= 0

    def play(self):
        while self.turn < 10:
            player_action = self.player_actions[self.turn]  # Get action from the player's sequence
            self.sequence += player_action
            
            
            enemy_action = ENEMY_ACTIONS[self.turn]
            
            if player_action != 'M' and not self.enemy_war_once:
                enemy_action = 'W'
                self.enemy_war_once = True
            
            self.enemy_sequence += enemy_action 

            self.calculate_points(player_action, enemy_action)

            self.turn += 1

        return self.player_points, self.enemy_points, self.sequence, self.enemy_sequence

def create_chromosome():
    """Create a random chromosome (action sequence)."""
    return ''.join(random.choices(ACTIONS, k=GENOME_LENGTH))

def create_population(size):
    """Initialize a random population of chromosomes."""
    return [create_chromosome() for _ in range(size)]

def fitness(chromosome):
    """Evaluate the fitness of a chromosome based on game simulation."""
    game = Game(chromosome) 
    player_points, enemy_points, sequence, enemy_sequence = game.play()

    return player_points - enemy_points, player_points, enemy_points, sequence, enemy_sequence

def tournament_selection(population):
    """Select two parents using tournament selection."""
    tournament_size = 5
    selected_parents = []

    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        tournament_winner = max(tournament, key=lambda chromo: fitness(chromo)[0])
        selected_parents.append(tournament_winner)

    return selected_parents

def crossover(parent1, parent2):
    """Apply single-point crossover to create offspring."""
    crossover_point = random.randint(1, GENOME_LENGTH - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

def mutate(chromosome):
    """Mutate a chromosome based on mutation rate."""
    new_chromosome = []
    for gene in chromosome:
        if random.random() < MUTATION_RATE:
            new_chromosome.append(random.choice(ACTIONS))  # Mutate to a new action
        else:
            new_chromosome.append(gene)
    return ''.join(new_chromosome)

def genetic_algorithm():
    """Run the genetic algorithm."""
    population = create_population(POPULATION_SIZE)

    for generation in range(GENERATIONS):
        print(f"\nGeneration {generation + 1}")

        population = sorted(population, key=lambda chromo: fitness(chromo)[0], reverse=True)

        best_chromosome = population[0]
        fitness_values = fitness(best_chromosome)  
        player_pts, enemy_pts, sequence, enemy_sequence = fitness_values[1:5]  

        print(f"Best sequence: {best_chromosome}, Fitness: {fitness_values[0]}")
        print(f"Your sequence: {sequence}, Enemy's sequence: {enemy_sequence}, Points (Player: {player_pts}, Enemy: {enemy_pts})")

        new_population = []

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = tournament_selection(population)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.extend([mutate(offspring1), mutate(offspring2)])

        population = new_population[:POPULATION_SIZE] 

if __name__ == "__main__":
    genetic_algorithm()
