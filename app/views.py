from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from . import models
from django.contrib import messages
from django.contrib.auth import authenticate, login as user_login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def fun(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_login(request, user)
            return redirect('fun')
        else:
            messages.info(request, 'username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def signup(request):
    if request.method == "GET":
        form = CreateUserForm()
        context = {"form": form}
        return render(request, 'signup.html', context=context)

    else:
        form = CreateUserForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            if user is not None:
                return redirect('login.html')

        else:
            return render(request, 'signup.html', context=context)


def signout(request):
    logout(request)
    return redirect('home')

