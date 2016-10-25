# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import authenticate as auth_authenticate, login as auth_login, logout as auth_logout
# from django.contrib import messages
#
# def login(request):
#     # get으로받은 이전경로 next에 저장
#     next = request.GET.get('next')
#     if request.method == "POST":
#         try:
#             username = request.POST['username']
#             password = request.POST['password']
#             # 데이터베이스와 계정일치여부 확인
#             # print(1)
#             user = auth_authenticate(username=username, password=password)
#             # print (user)
#         except KeyError:
#             return HttpResponse('username과 password는 필수입니다')
#
#         if user is not None:
#             # print(2)
#             # user 정보로 로그인처리
#             auth_login(request, user)
#             # message.level == DEFAULT_MESSAGE_LEVELS.SUCCESS
#             messages.success(request, "로그인 성공")
#             # 로그인 이전 화면으로 리다이렉트
#             return redirect(next)
#         else:
#             # message.level == DEFAULT_MESSAGE_LEVELS.ERROR
#             messages.error(request, "로그인 실패")
#             return render(request, 'member/login.html', {})
#     else:
#         # print(3)
#         return render(request, 'member/login.html')
#
#
# def logout(request):
#     auth_logout(request)
#     return redirect('blog:post_list')
#
