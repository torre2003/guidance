# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
import random


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('accounts:index'))
    context={}
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('accounts:index'))
            else:
                error = "Su cuenta está desactivada."
        else:
            error = 'Nombre de usuario o contraseña no válido.'
    imgs = [
        'accounts/login/img/1.jpg',
        'accounts/login/img/2.jpg',
        'accounts/login/img/3.jpg',
    ]
    random.shuffle(imgs)
    img_background = str(settings.STATIC_URL)+str(imgs[0])
    context['img_background'] = img_background
    context['error'] = error
    return render(request, 'accounts/login.html', context)

@login_required
def index_view(request):
    context = {}
    return render(request, 'accounts/index.html', context)


@login_required
def logout_view(request):
    logout(request)
    #messages.success(request, 'Te has desconectado con exito.')
    # eliminar datos de sesion asociados a distribuidor
    return redirect(reverse('accounts:login'))

