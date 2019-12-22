# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag("common/tag_menu.html")
def cod_menu():
    return {}


@register.inclusion_tag("common/tag_django_ajax.html")
def django_ajax():
    return {}

@register.inclusion_tag("common/source-datatable.html")
def css_dataTable():
    """
    Carga los archivos css y js utilizados por sparceDataTable.

    Params:
        botones= Indica si se deben cargar los js utilizados para generar los botones 
            "Copy", "CSV", Excel", "PDF", "Print".
        clase = Agrega clase/s extra/s al elemento <table>.
        identificador = Agrega un id al elemento <table>.
    """
    context = {}
    context['source'] = "css"
    return context

@register.inclusion_tag("common/source-datatable.html")
def js_dataTable(botones=None):
    """
    Carga los archivos css y js utilizados por sparceDataTable.

    Params:
        botones= Indica si se deben cargar los js utilizados para generar los botones 
            "Copy", "CSV", Excel", "PDF", "Print".
        clase = Agrega clase/s extra/s al elemento <table>.
        identificador = Agrega un id al elemento <table>.
    """

    context = {}
    context['source'] = "js"
    context['botones'] = botones
    return context

@register.assignment_tag
def div_dataTable(identificador='', clase=''):
    if clase:
        clase = ' ' + clase
    if identificador:
        identificador = ' id="' + identificador + '"'
    tabla = '<div class="table-responsive"><table' + identificador + ' class="table responsive table-hover table-striped dataTable js-exportable' + clase + '"></table></div>'
    return mark_safe(tabla)