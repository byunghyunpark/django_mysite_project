from django.contrib.auth import get_user_model
# 함수 호출해서 return 값을 User에 넣는
User = get_user_model()
# 윗 두줄은 아래 한줄과 같은 의미
# from member.models import MyUser as User

class FacebookBackend:
    def authenticate(self, user_info, token=None):
        # 계정이 있으면 로그인한다
        try:
            user = User.objects.get(facebook_id=user_info.get('id'))
            return user
        # 계정을 생성한다
        except User.DoesNotExist:
            user = User.objects.create_facebook_user(user_info)
            return user
    # authenticate 내부적으로 쓰이는 함수 필수 적으로 선언해야한다
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
