from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name='index'),

    ## Game

    # Get
    path('tictactoe/', views.get_stats, name='get_stats'),
    path('tictactoe/games/', views.get_all_games, name='get_all_games'),
    path('tictactoe/games/<int:game_id>/', views.get_one_game, name='get_one_game'),

    # Post
    path('tictactoe/games/create/', views.create_game, name='create_game'),

    # Patch
    path('tictactoe/games/<int:game_id>/join/', views.join_game, name='join_game'),

    # Post
    path('tictactoe/games/<int:game_id>/play/', views.game_play, name='game_play'),

    ## Auth

    # Post
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),

    # Get
    path('auth/logout/', views.logout, name='logout'),
]
