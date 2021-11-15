from django import template
from django.db.models import Count
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='add_class')
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
        })
    
@register.filter(name='get_val')
def get_val(dict, key):
    return dict.get(key)

@register.filter(name='read_more')
@stringfilter
def read_more(value):
    pattern = "<!--more-->"
    return value.split(pattern, 1)[0]