# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from apps import CommonConfig

@login_required
def view_datatable(request):
    context = {}
    context["id"] = request.POST.get('id', '')
    context["clases"] = request.POST.get('clases', '')
    context['titulo'] = request.POST.get('titulo', '')
    return render(request, CommonConfig.name+'/container_datatable.html', context)