from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


def login_home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                logout(request)
                login(request, user)
                url = 'home'
                nxt = request.GET.get("next", None)

                if nxt:
                    url = nxt
                return redirect(url)
            else:
                url = '/login/no_account'

                nxt = request.GET.get("next")

                print(nxt)

                if nxt:
                    url += f'?next={nxt}'

                return redirect(url)

        else:
            error = 'NOT CORRECT DATA'



    form = LoginForm()

    data = {
        'form' : form,
        'login' : login
    }
    return render(request, 'login/login_home.html', data)

def sign_up(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                logout(request)
                login(request, user)
                url = 'home'
                nxt = request.GET.get("next", None)

                if nxt:
                    url = nxt
                return redirect(url)
        else:
            error = 'NOT CORRECT DATA'



    form = LoginForm()

    data = {
        'form' : form
    }
    return render(request, 'login/sign_up.html', data)
