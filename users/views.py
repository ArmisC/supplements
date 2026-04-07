from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.urls import reverse

from users.models import User


def signup(request):
    if request.method == 'POST':
        error_messages = {}
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')


        if min(len(password), len(password_confirm)) < 8:
            error_messages['password_error'] = 'password should have more than 7 characters'
        if password != password_confirm:
            error_messages['password_error'] = 'passwords don\'t match'

        user, created = User.objects.get_or_create(email=email, defaults={'password': make_password(password), })
        if not created:
            error_messages['email'] = 'User with this email already exists'

        return redirect("users:login")
    elif request.method == 'GET':
        return render(request, 'users/signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = User.authenticate(email, password)

        if user:
            user.login(request)
            return redirect(reverse('home'))
        return render(request, 'users/login.html',context={'error': 'Credentials don\'t match'})
    return render(request, 'users/login.html')

def logout(request, pk):
    User.objects.get(pk=pk).logout(request)
    return redirect(reverse('home'))
