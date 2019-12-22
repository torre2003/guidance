# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime

register = template.Library()
dias_bdd={
    '1':'Domingo',
    '2':'Lunes',
    '3':'Martes',
    '4':'Miércoles',
    '5':'Jueves',
    '6':'Viernes',
    '7':'Sábado',
}

dias_python={
    '0':'Lunes',
    '1':'Martes',
    '2':'Miércoles',
    '3':'Jueves',
    '4':'Viernes',
    '5':'Sábado',
    '6':'Domingo',
}

dias_python_ab={
    '0':'Lu',
    '1':'Ma',
    '2':'Mi',
    '3':'Ju',
    '4':'Vi',
    '5':'Sá',
    '6':'Do',
}

@register.filter
def nombre_dia(html_input):
    """
    Inserta propiedades en un campo html.

    Uso: {{ form.field_name|add:'class="form-control" placeholder="Placeholder here"' }}
    """
    #print 'DIA: ',html_input,dias[str(html_input)]
    return mark_safe(dias_bdd[str(html_input)])


@register.filter
def puntuacion_valores(html_input):
    try:
        bandera = 1
        valor = int(html_input)
        if valor < 0:
            bandera = -1
        valor = abs(valor)
        aux = []
        i=0
        while i < valor:
            aux.append(bandera)
            i += 10
        return aux
    except Exception, e:
        print e
        return ''

@register.inclusion_tag("reporte/test_dashboard.html")
def puntuacion():
    return {'products_list': ['a','b','c'] }


@register.filter
def nombre_dia_en_fecha(html_input, es_abreviado=False):
    """
    print '*'*20
    print html_input
    print type(html_input)
    print '*'*20
    print 'html_input',html_input.year,' - ',es_abreviado
    """
    this_date = None
    try:
        if str(type(html_input)) == "<type 'datetime.date'>":
            this_date = html_input
        else:
            this_date = datetime.date(datetime.strptime(html_input, '%Y-%m-%d'))
        if es_abreviado:
            return dias_python_ab[str(datetime.weekday(this_date))]
        return dias_python[str(datetime.weekday(this_date))]
    except Exception, e:
        print e
        return ''
