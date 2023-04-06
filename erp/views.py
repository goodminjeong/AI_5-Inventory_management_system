from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/')
    else:
        return redirect('/login')