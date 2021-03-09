import numpy as np
import random
import Costants as const


class Game2048:
    def __init__(self):
        N = const.N
        self.grid = np.zeros((N, N), dtype=int)
        self.generate_new_number(n=2)
        self.score = 0

    def copy_grid(self):

        return self.grid.copy()

    def generate_new_number(self, n=1):
        free_positions = list(zip(*np.where(self.grid == 0)))
        if len(free_positions) > 0:
            for position in random.sample(free_positions, k=n):
                if random.random() <= .1:
                    self.grid[position] = 4
                else:
                    self.grid[position] = 2

    def move_left_and_sum(self, grid):
        score = 0
        for i in range(const.N):
            row = grid[i, :]
            new_row = np.zeros_like(row)
            row_n = row[row != 0]
            new_numbers = list()
            skip = False

            for j in range(len(row_n)):
                if skip:
                    skip = False
                    continue
                if (j != len(row_n)-1) and (row_n[j] == row_n[j+1]):
                    new_number = row_n[j] * 2
                    score += new_number
                    skip = True
                else:
                    new_number = row_n[j]
                new_numbers.append(new_number)

            new_row[:len(new_numbers)] = np.array(new_numbers)
            grid[i, :] = new_row

        return grid, score

    def game_over(self):
        for move in const.moves[:4]:
            if self.move_possible(move):
                return False
        return True

    def win(self):
        return 2048 in self.grid

    def move_possible(self, move):
        return not np.array_equal(self.grid, self.make_move(move=move, test=True), equal_nan=False)

    def make_move(self, move, test=False):
        if move == 'left':
            new_grid, score = self.move_left_and_sum(self.copy_grid())

        elif move == 'up':
            rot_grid, score = self.move_left_and_sum(np.rot90(self.copy_grid()))
            new_grid = np.rot90(rot_grid, -1)

        elif move == 'down':
            rot_grid, score = self.move_left_and_sum(np.rot90(self.copy_grid(), -1))
            new_grid = np.rot90(rot_grid)

        elif move == 'right':
            rot_grid, score = self.move_left_and_sum(np.rot90(self.copy_grid(), 2))
            new_grid = np.rot90(rot_grid, 2)

        elif move == 'restart':
            self.grid = np.zeros_like(self.copy_grid())
            self.generate_new_number(n=2)
            self.score = 0
            return

        if test:
            return new_grid
        else:
            self.grid = new_grid.copy()
            self.score += score if score else 0
            self.generate_new_number()
