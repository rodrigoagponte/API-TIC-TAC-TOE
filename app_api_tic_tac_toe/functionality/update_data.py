import datetime
from ..models import Game
import ast


def create_new_game_data(user):
    new_game = Game.objects.create(
        created_at=datetime.datetime.now().isoformat(),
        creator=user,
    )

    new_game.game_name = f'{user.username}#{new_game.id}'  # saving game name here, because it requires the game id
    save_data(game=new_game)
    return new_game


def join_game_update_data(game, user):
    game.wg_is_creator_turn = True
    game.wg_board_state = ["", "", "", "", "", "", "", "", ""]
    game.started_at = datetime.datetime.now().isoformat()

    game.opponent = user
    game.creator.games_waiting_move_count += 1

    save_data(game=game, creator=game.creator)


def applied_move_update_data(game_instance, game, user):

    if game_instance.current_board.count("") == 8:  # ONLY TRIGGERED IF THIS IS THE ABSOLUTE FIRST MOVE OF THIS GAME
        game.wg_plays = []  # create an empty list to log moves
    else:
        # if it's not the first move, this means the list of move (i.e. wg_plays) already has moves logged
        # which comes from django reading the database
        # in this case, we have to convert a string representation of a list into a type list
        game.wg_plays = ast.literal_eval(game.wg_plays)

    game.wg_plays.append(game_instance.current_board)  # log move into the moves list and place it in the database
    game.wg_board_state = game_instance.current_board  # update board state
    game.wg_total_moves += 1

    if user == game.creator:
        game.wg_is_creator_turn = False
        game.creator.games_waiting_move_count -= 1
        game.opponent.games_waiting_move_count += 1

    if user == game.opponent:
        game.wg_is_creator_turn = True
        game.creator.games_waiting_move_count += 1
        game.opponent.games_waiting_move_count -= 1

    save_data(game=game, creator=game.creator, opponent=game.opponent)


def endgame_update_data(user, game):
    if user == game.creator:
        game.opponent.games_waiting_move_count -= 1
    if user == game.opponent:
        game.creator.games_waiting_move_count -= 1

    game.wg_is_creator_turn = None
    game.ended_at = datetime.datetime.now().isoformat()

    save_data(game=game, creator=game.creator, opponent=game.opponent)


def winning_update_data(user, game):
    game.winner_id = user.id

    game.creator.total_games_played += 1
    game.opponent.total_games_played += 1

    if user == game.creator:
        game.creator.wins_count += 1
        game.opponent.losses_count += 1

    if user == game.opponent:
        game.creator.losses_count += 1
        game.opponent.wins_count += 1

    save_data(game=game, creator=game.creator, opponent=game.opponent)


def tie_update_data(game):
    game.creator.draws_count += 1
    game.opponent.draws_count += 1

    game.creator.total_games_played += 1
    game.opponent.total_games_played += 1

    save_data(creator=game.creator, opponent=game.opponent)


def save_data(game=None, creator=None, opponent=None):
    if game:
        game.save()
    if creator:
        creator.save()
    if opponent:
        opponent.save()
