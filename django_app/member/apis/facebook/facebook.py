from django.conf import settings
import requests
import json

__all__ = [
    'get_access_token',
    'get_debug_token',
    'get_user_info',
    'get_user_id_from_token',
]

# 통신할필요없는 고정값
APP_ID = settings.FACEBOOK_APP_ID
SECRET_CODE = settings.FACEBOOK_SECRET_CODE

APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE,
    )


def get_access_token(code, REDIRECT_URL):
    """
    access token을 받아내자
    :param code:
    :param REDIRECT_URL:
    :return:
    """
    url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?' \
                               'client_id={client_id}&' \
                               'redirect_uri={redirect_uri}&' \
                               'client_secret={client_secret}&' \
                               'code={code}'.format(
        client_id=APP_ID,
        redirect_uri=REDIRECT_URL,
        client_secret=SECRET_CODE,
        code=code,
    )
    # 해당 url로 get 요청을 보냄
    r = requests.get(url_request_access_token)
    dict_access_token = r.json()
    print(json.dumps(dict_access_token, indent=2))
    access_token = dict_access_token['access_token']
    return access_token


def get_debug_token(access_token):
    """
    debug token을 받아내자
    :param access_token:
    :return:
    """

    ACCESS_TOKEN = access_token

    url_debug_token = 'https://graph.facebook.com/debug_token?' \
                      'input_token={it}&' \
                      'access_token={at}'.format(
        it=ACCESS_TOKEN,
        at=APP_ACCESS_TOKEN
    )

    r = requests.get(url_debug_token)
    dict_debug = r.json()
    print(json.dumps(dict_debug, indent=2))
    return dict_debug


def get_user_id_from_token(access_token):
    """
    dict_debug에서 user_id를 추출
    :param access_token:
    :return:
    """
    debug_info = get_debug_token(access_token)
    user_id = debug_info['data']['user_id']
    return user_id


def get_user_info(user_id, access_token):
    """
    유저의 정보를 받아내자
    페이북에서 데이터 요청시 그래프 api 를 활용한다
    :param user_id:
    :param access_token:
    :return:
    """
    ACCESS_TOKEN = access_token
    USER_ID = user_id

    url_request_user_info = 'https://graph.facebook.com/' \
                            '{user_id}?' \
                            'fields=id,picture,name,first_name,last_name,timezone,email,birthday&' \
                            'access_token={access_token}'.format(
        user_id=USER_ID,
        access_token=ACCESS_TOKEN,
    )

    r = requests.get(url_request_user_info)
    dict_user_info = r.json()
    print(json.dumps(dict_user_info, indent=2))
    return dict_user_info


