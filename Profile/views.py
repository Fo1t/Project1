from django.shortcuts import render, redirect
from Profile.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



def Login(request):
    data = {'msg': ' '}
    data['form'] = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    data['msg'] = 'Disabled account'
                    return render(request, 'login.html', data)
            else:
                data['msg'] = 'Пользователь не существует'
                return render(request, 'login.html', data)
    return render(request, 'login.html', data)


def Registraion(request):
    data = {'msg': ' '}
    data['form'] = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']):
                data['msg'] = 'Пользователь с этим именем уже существует'
                return render(request, 'registration.html', data)
            if cd['password1'] != cd['password2']:
                data['msg'] = 'Пароли не совпадают'
                return render(request, 'registration.html', data)
            new_user = User(
                username=cd['username'],
                password=make_password(cd['password1'])
            )
            new_user.save()
            login(request, new_user)
            return redirect('/')
        else:
            return render(request, 'registration.html', data)
    return render(request, 'registration.html', data)
            
            