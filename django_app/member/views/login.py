from django.contrib import messages
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apis import facebook


def login(request):
    # get으로받은 이전경로 next에 저장
    next = request.GET.get('next')
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            # 데이터베이스와 계정일치여부 확인
            # print(1)
            user = auth_authenticate(username=username, password=password)
            # print (user)
        except KeyError:
            return HttpResponse('username과 password는 필수입니다')

        if user is not None:
            # print(2)
            # user 정보로 로그인처리
            auth_login(request, user)
            # message.level == DEFAULT_MESSAGE_LEVELS.SUCCESS
            messages.success(request, "로그인 성공")
            # 로그인 이전 화면으로 리다이렉트
            return redirect(next)
        else:
            # message.level == DEFAULT_MESSAGE_LEVELS.ERROR
            messages.error(request, "로그인 실패")
            return render(request, 'member/login.html', {})
    else:
        # print(3)
        return render(request, 'member/login.html')



def login_facebook(request):

    if request.GET.get('error'):
        messages.error(request, '페이스북 로그인을 취소했습니다')
        return redirect('member:login')

    if request.GET.get('code'):

        code = request.GET.get('code')
        REDIRECT_URL = 'http://127.0.0.1:8000/member/login/facebook/'

        # 모듈화 작업함함
        access_token = facebook.get_access_token(code, REDIRECT_URL)
        user_id = facebook.get_user_id_from_token(access_token)
        dict_user_info = facebook.get_user_info(user_id, access_token)


        # 유저를 인증하고 로그인시키자
        user = auth_authenticate(user_info=dict_user_info)
        if user is not None:
            auth_login(request, user)
            messages.success(request, '페이스북 로그인 성공')
            return redirect('blog:post_list')
        else:
            messages.error(request, '페이스북 로그인 실패')
            return redirect('member:login')