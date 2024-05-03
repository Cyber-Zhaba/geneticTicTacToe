import random


class Player:
    def __init__(self):
        self.genes = [0 for _ in range(9)]

    def move(self, board):
        valid_moves = [i for i in range(9) if board[i] == 0]
        return max(valid_moves, key=lambda i: self.genes[i])


class Game:
    def __init__(self, player1, player2):
        self.board = [0 for _ in range(9)]
        self.players = [player1, player2]
        self.current_player = 0

    def play(self):
        while True:
            move = self.players[self.current_player].move(self.board)
            self.board[move] = self.current_player + 1
            if (isinstance(self.players[self.current_player], HumanPlayer) or isinstance(
                    self.players[1 - self.current_player], HumanPlayer)):
                self.print_board()
            if self.check_win():
                return self.current_player
            self.current_player = 1 - self.current_player

    def print_board(self):
        symbols = ['.', 'X', 'O']
        print('\n' + '\n'.join([' '.join([symbols[self.board[i * 3 + j]] for j in range(3)]) for i in range(3)]) + '\n')

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
        while True:
            move = int(input("Enter your move (0-8): "))
            if move in valid_moves:
                return move
            else:
                print("Invalid move. Try again.")


class GeneticAlgorithm:
    def __init__(self, population_size):
        self.population = [Player() for _ in range(population_size)]

    def evolve(self, generations):
        for _ in range(generations):
            self.population = self.next_generation()

    def next_generation(self):
        winners = self.tournament_selection()
        children = self.breed(winners)
        return children

    def tournament_selection(self):
        winners = []
        for _ in range(len(self.population) // 2):
            player1, player2 = random.sample(self.population, 2)
            game = Game(player1, player2)
            winner = game.play()
            winners.append(self.population[winner])
        return winners

    def breed(self, winners):
        children = []
        for _ in range(len(self.population)):
            parent1, parent2 = random.sample(winners, 2)
            child = Player()
            for i in range(9):
                child.genes[i] = parent1.genes[i] if random.random() < 0.5 else parent2.genes[i]
            children.append(child)
        return children

    def play_against_human(self):
        human = HumanPlayer()
        best_ai = self.get_best_ai()
        game = Game(human, best_ai)
        winner = game.play()
        if winner == 0:
            print("Congratulations! You won against the AI.")
        else:
            print("The AI won. Better luck next time.")

    def get_best_ai(self):
        best_ai = max(self.population, key=self.evaluate)
        return best_ai

    @staticmethod
    def evaluate(player):
        wins = 0
        for _ in range(100):  # play 100 games to evaluate
            game = Game(player, Player())
            if game.play() == 0:
                wins += 1
        return wins


ga = GeneticAlgorithm(100)
ga.evolve(1000)
ga.play_against_human()
