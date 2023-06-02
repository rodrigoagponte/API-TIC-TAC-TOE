from .visualization import get_full_game_dict


def send_register_message(input_code, username=None):
    register_messages_dict = {
        '400AUTH1': {'code': '400AUTH1', 'details': 'Please provide a username'},
        '400AUTH2': {'code': '400AUTH2', 'details': 'Please provide a password'},
        '400AUTH3': {'code': '400AUTH3', 'details': 'Please provide an email'},
        '201AUTH1': {'code': '201AUTH1', 'details': 'Registration was successful', 'username': username}
    }
    return register_messages_dict[input_code]


def send_login_message(input_code, token=None):
    login_messages_dict = {
        '400AUTH1': {'code': '400AUTH1', 'details': 'Please provide a username'},
        '400AUTH2': {'code': '400AUTH2', 'details': 'Please provide a password'},
        '401AUTH1': {'code': '401AUTH1', 'details': 'Wrong Username or Password'},
        '200AUTH1': {'code': '200AUTH1', 'details': 'User logged in successfully', 'jwt': str(token)},
    }
    return login_messages_dict[input_code]


def send_logout_message(input_code):
    logout_messages_dict = {
        '400AUTH4': {'code': '400AUTH4', 'details': 'No user was logged in'},
        '200AUTH3': {'code': '200AUTH3', 'details': 'User logged out successfully'},
    }
    return logout_messages_dict[input_code]


def send_non_authentication_message(input_code):
    non_auth_dict = {
      '401AUTH5': {'code': '401AUTH5', 'details': 'Missing HTTP_AUTHORIZATION - Please login to get a Token'},
      '401AUTH4': {'code': '401AUTH4', 'details': 'Expired Signature Token - Please login to get a new Token'},
      '401AUTH2': {'code': '401AUTH2', 'details': 'Invalid Token - Please login to get a new Token'},
      '401AUTH3': {'code': '401AUTH3', 'details': 'Invalid Signature Token - Please login to get a new Token'},
    }
    return non_auth_dict[input_code]


def send_invalid_user_input_messages(input_code):
    invalid_user_input_dict = {
        '400GAME1': {'code': '400GAME1', 'details': 'Provide a valid action on a json object in the request body'},
        '400GAME2': {'code': '400GAME2', 'details': 'Check your input and try again'},
    }
    return invalid_user_input_dict[input_code]


def send_found_game_details_dict(input_code, user, game, playing_against=None, board=None):
    found_game_details_dict = {
        '200GAMEB': {'code': '200GAMEB',
                     'details': f"This game has ended",
                     'username': user.username, 'game': get_full_game_dict(game, user)},
        '200GAMEA': {'code': '200GAMEA',
                     'details': f"You've created this game but there is no opponent yet",
                     'username': user.username, 'game': get_full_game_dict(game, user)},
        '200GAME7': {'code': '200GAME7',
                     'details': f'The requested game is available to be joined',
                     'username': user.username, 'game': get_full_game_dict(game, user)},
        '200GAME8': {'code': '200GAME8',
                     'details': f"You are playing against **{playing_against}**. It's your turn to play",
                     'username': user.username, 'game': get_full_game_dict(game, user), 'board': board},
        '200GAME9': {'code': '200GAME9',
                     'details': f"You are playing against **{playing_against}**. It's NOT your turn to play",
                     'username': user.username, 'game': get_full_game_dict(game, user), 'board': board},
    }
    return found_game_details_dict[input_code]


def send_game_message(input_code, user, game, board=None, user_selected_square_number=None):
    game_messages_dict = {
        '400GAME3': {'code': '400GAME3', 'details': 'Occupied. Please choose an empty position',
                     'username': user.username, 'game': get_full_game_dict(game, user)},
        '200GAME4': {'code': '200GAME4', 'details': f'The creator has won the game', 'username': user.username,
                     'game': get_full_game_dict(game, user), 'board': board},
        '200GAME5': {'code': '200GAME5', 'details': f'The opponent has won the game', 'username': user.username,
                     'game': get_full_game_dict(game, user), 'board': board},
        '200GAME6': {'code': '200GAME6', 'details': f'The game ended in a draw', 'username': user.username,
                     'game': get_full_game_dict(game, user), 'board': board},
        '200GAME3': {'code': '200GAME3', 'details': f'Mark was placed on position {user_selected_square_number}',
                     'username': user.username, 'game': get_full_game_dict(game, user), 'board': board}
    }
    return game_messages_dict[input_code]
