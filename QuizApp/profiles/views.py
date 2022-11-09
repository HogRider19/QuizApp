from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from django.views import View
from django.contrib.auth.models import User


class LoginUser(View):
    
    def get(self, request):
        return render(request, 'profiles/login.html', {'form': AuthenticationForm()})

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )

        if user is None:
            return render(request, 'profiles/login.html', {'form': AuthenticationForm(), 'error': 'Неправвельный логин или пароль!'})

        login(request, user)
        return redirect('home')


class LogoutUser(View):
    def post(self, request):
        logout(request)
        return redirect('login')



