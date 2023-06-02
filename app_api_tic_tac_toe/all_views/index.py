from django.http import JsonResponse


def index(request):
    response = {
        'code': '200INDEX',
        'details': 'All the available endpoints for this API.',
        'available_endpoints': [
            'tictactoe/',
            'tictactoe/games/',
            'tictactoe/games/<int:game_id>/',
            'tictactoe/games/create/',
            'tictactoe/games/<int:game_id>/join/',
            'tictactoe/games/<int:game_id>/play/',
            'auth/register/',
            'auth/login/',
            'auth/logout/',
            'debug/allplayers/',
            'debug/allgames/',
            'debug/createplayer/',
            'debug/creategame/',
            'debug/createendgame/',
            'debug/createtiegame/',
        ]}

    return JsonResponse(response)
