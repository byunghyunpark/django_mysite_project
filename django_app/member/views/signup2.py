from django.shortcuts import render, redirect
from django.contrib.auth import login
from member.forms import SignupModelForm


def signup2(request):
    context = {}
    if request.method == 'POST':
        form = SignupModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            # backend를 설정해줘야함
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('blog:post_list')
        context['form'] = form
    else:
        form = SignupModelForm()
        context['form'] = form
    return render(request, 'member/signup.html', context)