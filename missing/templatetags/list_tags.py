import math

from django import template

register = template.Library()

@register.filter
def split_list(value, size):
    value = list(value)
    size = int(size)
    for i in range(int(math.ceil(len(value) / float(size)))):
        yield value[i*size:i*size+size]
