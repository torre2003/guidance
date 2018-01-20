# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag("common/tag_menu.html")
def cod_menu():
    return {}