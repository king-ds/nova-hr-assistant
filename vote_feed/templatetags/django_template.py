# from django import template
# register = template.Library()

# @register.filter
# def list_item(List, i):
#     return List[int(i)]

from django import template
import math
register = template.Library()

@register.filter
def list_item(List, i):
    try:
        return List[i]
    except:
        return "Time not available"

@register.filter
def floor(value):
    return int(math.floor(value))