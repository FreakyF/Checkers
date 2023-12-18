from typing import List, Optional

from Checker import Checker


class Checkerboard:
    def __init__(self):
        self.grid: List[List[Optional[Checker]]] = [[None for _ in range(8)] for _ in range(8)]
        self.setup_checkers()

    def setup_checkers(self):
        for i in range(8):
            if i % 2 == 1:
                self.grid[1][i] = Checker('black')
                self.grid[5][i] = Checker('white')
                self.grid[7][i] = Checker('white')
            else:
                self.grid[0][i] = Checker('black')
                self.grid[6][i] = Checker('white')

    def display_board(self):
        for y in range(8):
            row = ''
            for x in range(8):
                checker = self.grid[y][x]
                if checker:
                    checker_char = 'B' if checker.color == 'black' else 'W'
                    checker_char = checker_char.lower() if checker.is_king else checker_char
                else:
                    checker_char = '.'
                row += checker_char + ' '
            print(f"{8 - y} |", row)
        print("    a b c d e f g h")

    def move_checker(self, from_x, from_y, to_x, to_y):
        checker = self.grid[from_y][from_x]
        self.grid[to_y][to_x] = checker
        self.grid[from_y][from_x] = None

        if to_y in [0, 7]:
            checker.promote_to_king()

        if abs(from_x - to_x) == 2:
            mid_x, mid_y = (from_x + to_x) // 2, (from_y + to_y) // 2
            self.grid[mid_y][mid_x] = None
            return True
        return False
