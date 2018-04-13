# -*- coding: utf-8 -*-
from __future__ import unicode_literals


dias_bdd={
    1:u'Domingo',
    2:u'Lunes',
    3:u'Martes',
    4:u'Miércoles',
    5:u'Jueves',
    6:u'Viernes',
    7:u'Sábado',
}

dias_python={
    0:u'Lunes',
    1:u'Martes',
    2:u'Miércoles',
    3:u'Jueves',
    4:u'Viernes',
    5:u'Sábado',
    6:u'Domingo',
}

dias_js={
    0:u'Domingo',
    1:u'Lunes',
    2:u'Martes',
    3:u'Miércoles',
    4:u'Jueves',
    5:u'Viernes',
    6:u'Sábado',
}

dias_bdd_segun_nombre={
    u'Domingo':1,
    u'Lunes':2,
    u'Martes':3,
    u'Miércoles':4,
    u'Jueves':5,
    u'Viernes':6,
    u'Sábado':7,
}

dias_python_segun_nombre={
    u'Lunes':0,
    u'Martes':1,
    u'Miércoles':2,
    u'Jueves':3,
    u'Viernes':4,
    u'Sábado':5,
    u'Domingo':6,
}

dias_js_segun_nombre={
    u'Domingo':0,
    u'Lunes':1,
    u'Martes':2,
    u'Miércoles':3,
    u'Jueves':4,
    u'Viernes':5,
    u'Sábado':6,
}

dias_python_ab={
    0:u'Lu',
    1:u'Ma',
    2:u'Mi',
    3:u'Ju',
    4:u'Vi',
    5:u'Sá',
    6:u'Do',
}

def arreglo_nombre_dias(dias,tipo):
    """
        Genera un arreglo con los nombres de los dias
        Params:
            dias[int,,]: numero de los dias
            tipo(string): formato de los dias
                'py': formato python
                'bdd': formato base de datos
                'js': formato javascripts
        Return
        []: Array con el nombre de los días
        None si no se especifica la codificación
    """
    nombre_dias = None
    if tipo == 'py':
        nombre_dias = dias_python
    elif tipo == 'bdd':
        nombre_dias = dias_bdd
    elif tipo == 'js':
        nombre_dias = dias_js
    else:
        return None
    aux = []
    for dia in dias:
        aux.append(nombre_dias[dia])
    return aux


def generar_diccionario_dias(dias, tipo):
    """
        Genera un diccionario detallado de los dias
        Params:
            dias[int,,]: numero de los dias
            tipo(string): formato de los dias
                'py': formato python
                'bdd': formato base de datos
                'js': formato javascripts
        Return
        {
            nombre:[string,,],
            js:[int,,],
            bdd:[int,,],
            js:[int,,]
        }
        None si no se especifica la codificación
    """
    nombre_dias = arreglo_nombre_dias(dias,tipo)
    aux = {
        'nombre':[],
        'py':[],
        'bdd':[],
        'js':[]
    }
    for nombre in nombre_dias:
        aux['nombre'].append(nombre)
        aux['py'].append(dias_python_segun_nombre[nombre])
        aux['bdd'].append(dias_bdd_segun_nombre[nombre])
        aux['js'].append(dias_js_segun_nombre[nombre])
    return aux

def formato_numero (numero, decimales=0):
    """
        Función que retorna un string con el numero formateado con puntos y comas
    """
    formato = "{0:,."+unicode(decimales)+"f}"
    return r_c_p(formato.format(numero))


def r_c_p (string):
    """
        Función que intercambia puntos por comas
    """
    aux = str(string).replace('.','X')
    aux = str(aux).replace(',','Y')
    aux = str(aux).replace('X',',')
    aux = str(aux).replace('Y','.')
    return aux


