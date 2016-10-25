from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login

from member.forms import SignupForm
from member.models import MyUser



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            nickname = request.POST['nickname']

            if password1 != password2:
                messages.error(request, "패스워드가 다릅니다")
                return redirect('member:signup')

            user = MyUser.objects.create_user(
                email=email,
                password=password1,
                last_name=last_name,
                first_name=first_name,
                nickname=nickname,
            )

            login(request, user)
            messages.success(request, "회원가입 성공")
            return redirect('blog:post_list')
        else:
            pass
    else:
        form = SignupForm()
    return render(request, 'member/signup.html', {'form': form})