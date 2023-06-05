from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Game, CustomUser

from ..functionality.helper_functions import find_user, find_game, get_games_dicts, get_found_game_details
from ..functionality.helper_functions import check_user_input_validity

from ..functionality.visualization import get_full_game_dict, get_game_info_dict, get_player_stats
from ..functionality.visualization import get_overall_game_stats, check_user_turn

from ..functionality.helper_data import send_invalid_user_input_messages, send_non_authentication_message
from ..functionality.helper_data import send_join_game_message, send_cannot_play_game_message
from ..functionality.authentication import process_bearer_token
from ..functionality.game_playing import user_made_move
from ..functionality.update_data import create_new_game_data, join_game_update_data


def get_stats(request):

    processed_bearer_token = process_bearer_token(request)
    if not processed_bearer_token['auth']:
        return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
    payload_username = processed_bearer_token['payload']['username']
    user = find_user(payload_username)

    success_response = {
        'code': '200GAME1',
        'details': 'Overall statistics',
        'username': user.username,
        'player_stats': get_player_stats(user, Game.objects.all()),
        "overall_game_stats": get_overall_game_stats(CustomUser.objects.all(), Game.objects.all()),
    }

    return JsonResponse(success_response)


def get_all_games(request):

    processed_bearer_token = process_bearer_token(request)
    if not processed_bearer_token['auth']:
        return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
    payload_username = processed_bearer_token['payload']['username']
    user = find_user(payload_username)

    my_games_dict, open_games_dict = get_games_dicts(user, Game.objects.all())

    success_response = {
      "code": "200GAME2",
      "details": "Player games",
      "username": user.username,
      "my_games": {
        "completed": [get_game_info_dict(game) for game in my_games_dict['completed']],
        "playing": [get_game_info_dict(game) for game in my_games_dict['playing']]
      },
      "open_games": {
        "by_me": [get_game_info_dict(game) for game in open_games_dict['by_me']],
        "by_others": [get_game_info_dict(game) for game in open_games_dict['by_others']]
      }
    }

    return JsonResponse(success_response)


def get_one_game(request, game_id):

    processed_bearer_token = process_bearer_token(request)
    if not processed_bearer_token['auth']:
        return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
    payload_username = processed_bearer_token['payload']['username']
    user = find_user(payload_username)

    game = find_game(game_id)
    if not game:
        return JsonResponse(
            {'code': '404GAME1', 'details': f"There's no game with the id {game_id}", 'username': user.username}
        )

    return JsonResponse(get_found_game_details(user, game))


@csrf_exempt
def create_game(request):
    if request.method == 'POST':

        processed_bearer_token = process_bearer_token(request)
        if not processed_bearer_token['auth']:
            return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
        payload_username = processed_bearer_token['payload']['username']
        user = find_user(payload_username)

        new_game = create_new_game_data(user)

        success_response = {
            'code': '201GAME1',
            'details': f'Game {new_game.game_name} created',
            'username': user.username,
            'game': get_full_game_dict(new_game, user),
        }
        return JsonResponse(success_response)


@csrf_exempt
def join_game(request, game_id):
    if request.method == 'PATCH':

        processed_bearer_token = process_bearer_token(request)
        if not processed_bearer_token['auth']:
            return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
        payload_username = processed_bearer_token['payload']['username']
        user = find_user(payload_username)

        game = find_game(game_id)
        if not game:
            return JsonResponse(send_join_game_message('404GAME1', game_id, user, game))

        if game.creator == user:
            return JsonResponse(send_join_game_message('403GAME2', game_id, user, game))

        if game.opponent:
            return JsonResponse(send_join_game_message('403GAME1', game_id, user, game))

        join_game_update_data(game, user)
        return JsonResponse(send_join_game_message('200GAMEC', game_id, user, game))


@csrf_exempt
def game_play(request, game_id):
    if request.method == 'POST':

        processed_bearer_token = process_bearer_token(request)
        if not processed_bearer_token['auth']:
            return JsonResponse(send_non_authentication_message(processed_bearer_token['code']))
        payload_username = processed_bearer_token['payload']['username']
        user = find_user(payload_username)

        game = find_game(game_id)
        if not game:
            return JsonResponse(send_cannot_play_game_message('404GAME1', game_id, user, game))

        if game.ended_at:
            return JsonResponse(send_cannot_play_game_message('403GAME3', game_id, user, game))

        if user not in [game.creator, game.opponent]:
            return JsonResponse(send_cannot_play_game_message('N/A', game_id, user, game))

        is_user_turn = check_user_turn(user, game)

        if not is_user_turn:
            return JsonResponse(send_cannot_play_game_message('403GAME4', game_id, user, game))

        user_selected_square_number = check_user_input_validity(request)

        if type(user_selected_square_number) != int:
            return JsonResponse(send_invalid_user_input_messages(user_selected_square_number['code']))

        return JsonResponse(user_made_move(user_selected_square_number, user, game))
