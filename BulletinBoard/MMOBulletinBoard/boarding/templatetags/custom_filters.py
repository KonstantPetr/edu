from django import template
from boarding.resources import *

register = template.Library()


@register.filter()
def nice_category(value):
    value = Category[value]
    return value


@register.filter()
def nice_status(value):
    value = Status[value]
    return value
