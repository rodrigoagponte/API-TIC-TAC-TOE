def check_user_turn(user, game):
    if not game.started_at or game.ended_at:
        return None
    if user == game.creator and game.wg_is_creator_turn:
        return True
    if user == game.opponent and not game.wg_is_creator_turn:
        return True
    return False


def can_user_join_game(game):
    if game.opponent:
        return False
    return True


def get_game_info_dict(input_game):
    opponent_dict = {}

    if input_game.opponent:
        opponent_dict = {
            'id': input_game.opponent.id,
            'username': input_game.opponent.username,
            'email': input_game.opponent.email
        }

    game_info_dict = {
            "id": input_game.id,
            "game_name": input_game.game_name,
            "wg_is_creator_turn": input_game.wg_is_creator_turn,
            "wg_total_moves": input_game.wg_total_moves,
            "wg_board_state": str(input_game.wg_board_state),
            "wg_plays": input_game.wg_plays,
            "created_at": input_game.created_at,
            "started_at": input_game.started_at,
            "ended_at": input_game.ended_at,
            "winner_id": input_game.winner_id,
            "creator": {
                "id": input_game.creator.id,
                "username": input_game.creator.username,
                "email": input_game.creator.email
            },
            "opponent": opponent_dict
        }
    return game_info_dict


def get_full_game_dict(game, user):
    game_dict = {
        "can_join": can_user_join_game(game),
        "is_my_turn": check_user_turn(user, game),
        "game_info": get_game_info_dict(game)
    }
    return game_dict


def render_board(board_state):
    if board_state == "":
        return None

    board = [
        f"[ {board_state[0]} | {board_state[1]} | {board_state[2]} ]",
        f"[───┼───┼───]",
        f"[ {board_state[3]} | {board_state[4]} | {board_state[5]} ]",
        f"[───┼───┼───]",
        f"[ {board_state[6]} | {board_state[7]} | {board_state[8]} ]"
    ]
    return board


def get_all_available_games_count(user, all_games):
    all_available_games_count = 0
    if all_games:
        for game in all_games:
            if can_user_join_game(game) and game.creator != user:
                all_available_games_count += 1
    return all_available_games_count


def get_player_stats(user, all_games):
    player_stats_dict = {
            'total_games_played': user.total_games_played,
            'wins_count': user.wins_count,
            'draws_count': user.draws_count,
            'losses_count': user.losses_count,
            'games_waiting_move_count': user.games_waiting_move_count,
            'available_games_count': get_all_available_games_count(user, all_games),
        }
    return player_stats_dict


def get_overall_game_stats(all_users, all_games):
    total_games_played_count = 0
    total_open_games_count = 0
    total_games_being_played = 0

    for game in all_games:

        if game.ended_at:
            total_games_played_count += 1

        if can_user_join_game(game):
            total_open_games_count += 1

        if not can_user_join_game(game) and not game.ended_at:
            total_games_being_played += 1

    game_stats_dict = {
        "total_players_registered_count": len(all_users),
        "total_games_played_count": total_games_played_count,
        "total_open_games_count": total_open_games_count,
        "total_games_being_played_count": total_games_being_played,
    }
    return game_stats_dict
