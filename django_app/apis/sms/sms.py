"""
coolsms 서비스 로그인
Azelf / dlgksdud1

http://www.coolsms.co.kr/Python_SDK_Start_here
"""
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

__all__ = [
    'send_sms',
]

api_key = 'NCS5805501D62D8B'
api_secret = 'A86DF83FB2F77AC52F0322A8B1B294A1'


def send_sms(message, receiver_number):
    if receiver_number is None or len(receiver_number) < 10:
        print('Receiver number invalid')
        return False
    params = dict()
    params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
    params['to'] = receiver_number # Recipients Number '01000000000,01000000001'
    params['from'] = '01029953874' # Sender number
    params['text'] = message # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print(response)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])
            return False
        return True

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
        return False