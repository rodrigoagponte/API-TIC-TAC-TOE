import ast
from .helper_data import send_game_message
from .visualization import render_board
from .update_data import endgame_update_data, winning_update_data, tie_update_data, applied_move_update_data
from .tic_tac_toe import TicTacToe, SquareIsOccupied


def get_current_player(user, game):
    if user == game.creator:
        return 'X'
    if user == game.opponent:
        return 'O'


def user_made_move(user_selected_square_number, user, game):
    # start by converting a string representation of a list into a type list
    horizontal_game_board = ast.literal_eval(game.wg_board_state)
    current_player = get_current_player(user, game)
    game_instance = TicTacToe(horizontal_game_board, current_player)

    try:
        game_instance.play(user_selected_square_number)
    except SquareIsOccupied:
        return send_game_message(input_code='400GAME3', user=user, game=game)

    applied_move_update_data(game_instance, game, user)

    board = render_board(game.wg_board_state)

    if game_instance.is_finished:
        endgame_update_data(user, game)

        if game_instance.found_winner:
            winning_update_data(user, game)
            if user == game.creator:
                return send_game_message(input_code='200GAME4', user=user, game=game, board=board)
            if user == game.opponent:
                return send_game_message(input_code='200GAME5', user=user, game=game, board=board)

        if game_instance.found_tie:
            tie_update_data(game)
            return send_game_message(input_code='200GAME6', user=user, game=game, board=board)

    return send_game_message(input_code='200GAME3', user=user, game=game, board=board,
                             user_selected_square_number=user_selected_square_number)
