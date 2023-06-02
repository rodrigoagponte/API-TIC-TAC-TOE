import datetime
import jwt
from jwt.exceptions import InvalidTokenError, InvalidSignatureError, ExpiredSignatureError


def create_access_token(user_id, username):
    now = datetime.datetime.utcnow()
    token = jwt.encode(
        payload={'user_id': user_id, 'username': username, 'exp': now + datetime.timedelta(minutes=120), 'iat': now},
        key='refresh_secret',
        algorithm='HS256'
    )
    return token


def check_for_bearer_token_existence(request):
    try:
        authorization = request.headers['Authorization']
        return authorization
    except KeyError:  # if there is no bearer token, the line above will return a KeyError
        return None


def process_bearer_token(request):
    authorization = check_for_bearer_token_existence(request)

    if not authorization:
        return {'auth': False, 'code': '401AUTH5'}

    try:
        token = authorization.split(' ')[1]  # remove the word "Bearer"
        decoded_payload = jwt.decode(token, key='refresh_secret', algorithms=['HS256', ])
        return {'auth': True, 'payload': decoded_payload}

    except ExpiredSignatureError:
        return {'auth': False, 'code': '401AUTH4'}

    except InvalidTokenError:
        return {'auth': False, 'code': '401AUTH2'}

    except InvalidSignatureError:
        return {'auth': False, 'code': '401AUTH3'}
