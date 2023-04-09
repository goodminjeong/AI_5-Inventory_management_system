from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
import re


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
            # 비밀번호가 같지 않은 경우 경고창
            return render(request, 'accounts/signup.html', {'error': '비밀번호를 확인해 주세요!'})
        else:
            if username == '' or password == '':
                # 이름이나 비밀번호가 빈칸인 경우 경고창
                return render(request, 'accounts/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값 입니다'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 이미 가입한 유저의 이름과 같은 경우 경고창
                return render(request, 'accounts/signup.html', {'error': '사용자가 존재합니다'})
            regex_email = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            if not re.fullmatch(regex_email, email):
                # 이메일 형식이 아닌 경우 경고창
                return render(request, 'accounts/signup.html', {'error': '올바른 이메일 형식이 아닙니다'})
            else:
                User.objects.create_user(
                    username=username, password=password, email=email)  # 회원가입 정보를 User모델에 저장
                return redirect('/login')  # 회원가입이 완료되면 로그인 페이지로 이동


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': '이름 혹은 비밀번호를 확인해 주세요!'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/login.html')
