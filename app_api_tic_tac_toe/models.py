from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=80)
    email = models.EmailField(unique=True)

    total_games_played = models.IntegerField(default=0)
    wins_count = models.IntegerField(default=0)
    draws_count = models.IntegerField(default=0)
    losses_count = models.IntegerField(default=0)
    games_waiting_move_count = models.IntegerField(default=0)
    available_games_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.username}'


class Game(models.Model):
    game_name = models.CharField(max_length=80, null=True, unique=True)

    wg_is_creator_turn = models.BooleanField(null=True, blank=True)
    wg_total_moves = models.IntegerField(default=0)
    wg_board_state = models.CharField(max_length=800, default="")  # displays the board
    wg_plays = models.CharField(max_length=800, default="")  # do not know what this is

    created_at = models.CharField(max_length=80, null=False)
    started_at = models.CharField(max_length=80, null=True)
    ended_at = models.CharField(max_length=80, null=True)

    winner_id = models.IntegerField(null=True)

    creator = models.ForeignKey("CustomUser", null=True, on_delete=models.SET_NULL, related_name='game_creator')
    opponent = models.ForeignKey("CustomUser", null=True, on_delete=models.SET_NULL, related_name='game_opponent')

    def __str__(self):
        return f'Game Name: {self.game_name} --- Game ID: {self.id}'

