class SquareIsOccupied(Exception):
    pass


class TicTacToe:
    WINNING_COMBINATIONS = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    def __init__(self, current_board, current_player):
        self.current_board = current_board
        self.current_player = current_player

        self.found_winner = False
        self.found_tie = False

    @property
    def is_finished(self):
        return self.found_winner or self.found_tie

    def check_for_winner(self):
        for combination in self.WINNING_COMBINATIONS:
            if all(
                self.current_board[index_number] == self.current_player
                for index_number in combination
            ):
                return True
        return False

    def check_for_tie(self):
        if not self.found_winner and all(element != "" for element in self.current_board):
            return True
        return False

    def play(self, square_number):
        assert not self.is_finished

        if self.current_board[square_number - 1] != "":
            raise SquareIsOccupied(square_number)

        self.current_board[square_number - 1] = self.current_player

        self.found_winner = self.check_for_winner()
        self.found_tie = self.check_for_tie()
