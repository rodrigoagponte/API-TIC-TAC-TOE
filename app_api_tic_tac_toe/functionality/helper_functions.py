from app_api_tic_tac_toe.models import CustomUser, Game
import ast
from .helper_data import send_found_game_details_dict
from .visualization import render_board, check_user_turn, can_user_join_game


def find_user(username, password=None):
    try:
        if not password:
            user = CustomUser.objects.get(username=username)
        else:
            user = CustomUser.objects.get(username=username, password=password)
        return user
    except CustomUser.DoesNotExist:
        return None


def find_game(game_id):
    try:
        return Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return None


def get_games_dicts(user, all_games):
    my_games_dict = {'completed': [], 'playing': []}
    open_games_dict = {'by_me': [], 'by_others': []}
    for game in all_games:
        # means the user in question is participating in said game, which means it goes to my_game_dict
        if game.creator == user or game.opponent == user:

            if game.ended_at:  # if it has ended, goes to completed
                my_games_dict['completed'].append(game)

            # if it has not ended, and cannot join means it is playing
            # there is the instance, right after creating the game when the game has not ended,
            # and there is the possibility to join. if that is the case, this will not be triggered
            if not game.ended_at and not can_user_join_game(game):
                my_games_dict['playing'].append(game)

        if can_user_join_game(game):
            if game.creator == user:
                open_games_dict['by_me'].append(game)
            else:
                open_games_dict['by_others'].append(game)

    return my_games_dict, open_games_dict


def check_who_is_the_user_playing_against(user, game):
    playing_against = None
    if user == game.creator:
        playing_against = game.opponent.username
    if user == game.opponent:
        playing_against = game.creator.username
    return playing_against


def get_found_game_details(user, game):
    try:
        # try, converting a string representation of a list into a type list
        board_state = ast.literal_eval(game.wg_board_state)
    except SyntaxError:
        # error occurs if wg_board_state = "" (i.e., no one has joined a game, no board has been created)
        board_state = ""

    board = render_board(board_state)

    if game.ended_at:
        return send_found_game_details_dict('200GAMEB', user, game)

    if can_user_join_game(game):
        if user == game.creator:
            return send_found_game_details_dict('200GAMEA', user, game)

        return send_found_game_details_dict('200GAME7', user, game)

    playing_against = check_who_is_the_user_playing_against(user, game)
    is_user_turn = check_user_turn(user, game)

    if is_user_turn:
        return send_found_game_details_dict('200GAME8', user, game, playing_against, board)

    if not is_user_turn:
        return send_found_game_details_dict('200GAME9', user, game, playing_against, board)


def check_user_input_validity(request):
    try:
        user_selected_square_number = float(request.POST.get('square_number'))
    except TypeError:
        return {'code': '400GAME2'}
    except ValueError:
        return {'code': '400GAME2'}

    if user_selected_square_number % 1 != 0:
        return {'code': '400GAME2'}

    user_selected_square_number = int(user_selected_square_number)

    if user_selected_square_number > 9 or user_selected_square_number < 1:
        return {'code': '400GAME2'}

    return user_selected_square_number
