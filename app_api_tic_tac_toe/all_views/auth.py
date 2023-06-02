import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_api_tic_tac_toe.functionality.helper_functions import find_user
from ..functionality.authentication import create_access_token, check_for_bearer_token_existence
from ..models import CustomUser
from ..functionality.helper_data import send_register_message, send_login_message, send_logout_message


@csrf_exempt
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username:
            return JsonResponse(send_register_message('400AUTH1'))

        if not password:
            return JsonResponse(send_register_message('400AUTH2'))

        if not email:
            return JsonResponse(send_register_message('400AUTH3'))

        CustomUser.objects.create(username=username, password=password, email=email)
        return JsonResponse(send_register_message('201AUTH1', username))


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            return JsonResponse(send_login_message('400AUTH1'))

        if not password:
            return JsonResponse(send_login_message('400AUTH2'))

        user = find_user(username=username, password=password)

        if not user:
            return JsonResponse(send_login_message('401AUTH1'))

        token = create_access_token(user.id, user.username)
        return JsonResponse(send_login_message('200AUTH1', token))


@csrf_exempt
def logout(request):

    authorization = check_for_bearer_token_existence(request)

    if not authorization:
        return JsonResponse(send_logout_message('400AUTH4'))

    token = authorization.split(' ')[1]  # remove the word "Bearer"

    # returns the payload from the created the token
    decoded_payload = jwt.decode(token, key='refresh_secret', algorithms=['HS256', ])

    user = find_user(username=decoded_payload['username'])

    if user:
        return JsonResponse(send_logout_message('200AUTH3'))

    return JsonResponse(send_logout_message('400AUTH4'))
