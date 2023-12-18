from Checkerboard import Checkerboard


def get_player_move(color):
    while True:
        print(f"Player {color}'s turn. Enter move (e.g., 'b6 c5'): ")
        try:
            move_input = input()
            move = move_input.split()
            if len(move) != 2 or len(move[0]) != 2 or len(move[1]) != 2:
                raise ValueError("Invalid move format")

            from_x, from_y = ord(move[0][0]) - ord('a'), 8 - int(move[0][1])
            to_x, to_y = ord(move[1][0]) - ord('a'), 8 - int(move[1][1])

            if from_x < 0 or from_x > 7 or from_y < 0 or from_y > 7 or to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
                raise ValueError("Move out of bounds")

            return from_x, from_y, to_x, to_y

        except (ValueError, IndexError):
            print("Invalid move. Try again.")


class CheckersGame:
    def __init__(self):
        self.board = Checkerboard()
        self.current_player = 'white'

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_valid_move(self, from_x, from_y, to_x, to_y):
        if from_x < 0 or from_x > 7 or from_y < 0 or from_y > 7 or to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
            return False

        checker = self.board.grid[from_y][from_x]
        if not checker or checker.color != self.current_player:
            return False

        dx, dy = to_x - from_x, to_y - from_y
        if abs(dx) != abs(dy):
            return False  # Move must be diagonal

        if not checker.is_king:
            direction = -1 if checker.color == 'white' else 1
            if dy != direction and abs(dy) != 2:  # One square forward or capture move
                return False

        if checker.is_king:
            enemy_color = None

            step_x = 1 if to_x > from_x else -1
            step_y = 1 if to_y > from_y else -1
            x, y = from_x + step_x, from_y + step_y
            encountered_enemy = False
            passed_enemy = False

            while x != to_x or y != to_y:
                if self.board.grid[y][x] is not None:
                    if encountered_enemy:
                        return False  # More than one checker encountered
                    encountered_enemy = True
                    enemy_color = self.board.grid[y][x].color

                if encountered_enemy and not passed_enemy:
                    passed_enemy = True  # Passed the enemy checker
                elif passed_enemy and self.board.grid[y][x] is not None:
                    return False  # Space after enemy checker is not empty

                x += step_x
                y += step_y

            if encountered_enemy and checker.color != enemy_color and not passed_enemy:
                return False  # Must be empty space after captured checker

        return True

    def player_has_checkers(self, color):
        for row in self.board.grid:
            for checker in row:
                if checker and checker.color == color:
                    return True
        return False

    def player_has_moves(self, color):
        for y in range(8):
            for x in range(8):
                checker = self.board.grid[y][x]
                if checker and checker.color == color:
                    if self.checker_can_move(x, y):
                        return True
        return False

    def checker_can_move(self, x, y):
        checker = self.board.grid[y][x]
        if not checker:
            return False

        move_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if not checker.is_king:
            move_offsets = move_offsets[:2] if checker.color == 'white' else move_offsets[2:]

        for dx, dy in move_offsets:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_move(x, y, new_x, new_y):
                return True

            capture_x, capture_y = x + 2 * dx, y + 2 * dy
            if self.is_valid_move(x, y, capture_x, capture_y):
                return True

        return False

    def check_game_over(self):
        if not self.player_has_checkers('white'):
            print("Black wins!")
            return True
        if not self.player_has_checkers('black'):
            print("White wins!")
            return True
        return False

    def play(self):
        game_over = False
        while not game_over:
            self.board.display_board()
            from_x, from_y, to_x, to_y = get_player_move(self.current_player)

            if self.is_valid_move(from_x, from_y, to_x, to_y):
                self.board.move_checker(from_x, from_y, to_x, to_y)
                self.switch_player()
            else:
                print("Invalid move. Try again.")

            if not self.player_has_moves(self.current_player):
                game_over = self.check_game_over()
