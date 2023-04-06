from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')

        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'accounts/signup.html', {'error': '비밀번호를 확인해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'accounts/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'accounts/signup.html', {'error': '사용자가 존재합니다'})
            else:
                User.objects.create_user(
                    username=username, password=password, email=email)
                return redirect('/login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return render(request, 'erp/home.html')
        else:
            return render(request, 'accounts/login.html', {'error': '이름 혹은 비밀번호를 확인해 주세요!'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
