import random


class Player:
    def __init__(self):
        self.genes = [0 for _ in range(9)]

    def move(self, board):
        valid_moves = [i for i in range(9) if board[i] == 0]
        if valid_moves:
            return max(valid_moves, key=lambda i: self.genes[i])
        return None


class Game:
    def __init__(self, player1, player2):
        self.board = [0 for _ in range(9)]
        self.players = [player1, player2]
        self.current_player = 0

    def play(self):
        while True:
            move = self.players[self.current_player].move(self.board)
            if move is None:
                return None
            self.board[move] = self.current_player + 1
            if (isinstance(self.players[self.current_player], HumanPlayer) or isinstance(
                    self.players[1 - self.current_player], HumanPlayer)):
                self.print_board()
            if self.check_win():
                return self.current_player
            self.current_player = 1 - self.current_player

    def print_board(self):
        symbols = ['.', 'X', 'O']
        print('\n' + '\n'.join([' '.join([symbols[self.board[i * 3 + j]] for j in range(3)]) for i in range(3)]))

    def check_win(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != 0:
                return True
        return False


class HumanPlayer:
    @staticmethod
    def move(board):
        valid_moves = [i for i in range(9) if board[i] == 0]
        while valid_moves:
            move = int(input("Enter your move (0-8): "))
            if move in valid_moves:
                return move
            else:
                print("Invalid move. Try again.")


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate=0.01, elitism_size=2):
        self.population = [Player() for _ in range(population_size)]
        self.mutation_rate = mutation_rate
        self.elitism_size = elitism_size

    def evolve(self, generations):
        for gen in range(generations):
            progres = f"|{"-" * (20 * gen // generations):<20}| {gen}/{generations}"
            print(progres, end="")
            self.population = self.next_generation()
            print("\b" * len(progres), end="")

    def next_generation(self):
        winners = self.tournament_selection()
        children = self.breed(winners)
        self.mutate(children)
        return children

    @staticmethod
    def crossover(parent1, parent2):
        child = Player()
        for i in range(9):
            child.genes[i] = parent1.genes[i] if random.random() < 0.5 else parent2.genes[i]
        return child

    def breed(self, winners):
        children = []
        for _ in range(len(self.population)):
            parent1, parent2 = random.sample(winners, 2)
            child = self.crossover(parent1, parent2)
            children.append(child)
        return children

    def mutate(self, children):
        for child in children:
            if random.random() < self.mutation_rate:
                child.genes[random.randint(0, 8)] = random.random()

    def tournament_selection(self):
        players = self.population
        winners = []
        while len(players) > 10:
            winners = []
            for i in range(len(players) - 1):
                player1, player2 = players[i:i+2]
                game = Game(player1, player2)
                winner = game.play()
                if winner is not None:
                    winners.append([player1, player2][winner])
            if len(winners) > 1:
                players = winners
        return winners

    def play_against_human(self, player_choice):
        human = HumanPlayer()
        best_ai = self.get_best_ai()
        if player_choice == "X":
            game = Game(human, best_ai)
        else:
            game = Game(best_ai, human)
        winner = game.play()
        if (winner == 0 and player_choice == "X") or (winner == 1 and player_choice != "X"):
            print("Congratulations! You won against the AI.")
        elif winner:
            print("The AI won. Better luck next time.")
        else:
            print("Nobody won")

    def get_best_ai(self):
        best_ai = self.population[0]
        for i in range(1, len(self.population)):
            player2 = self.population[i]
            game = Game(best_ai, player2)
            winner = game.play()
            if winner is None:
                winner = 0
            best_ai = [best_ai, player2][winner]
        return best_ai


ga = GeneticAlgorithm(400)
ga.evolve(500)
while input("Play with ai? [y]/[n]\n") == "y":
    choice = input("X or O?\n")
    ga.play_against_human(choice)
