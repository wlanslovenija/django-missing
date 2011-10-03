import math

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def split_list(value, length):
    """
    Splits input list into sublists of the given length.
    
    Last sublist can be shorter if input list length is not a multiplier of the given length.

    Sample usage::

        {% for group in objects|split_list:"4" %}
            <tr>
            {% for obj in group %}
                <td>{{ obj }}</td>
            {% endfor %}
            </tr>
        {% endfor %}
    """

    try:
        value = list(value)
        length = int(length)

        if not length:
            return

        for i in range(int(math.ceil(len(value) / float(length)))):
            yield value[i*length:i*length+length]
    except:
        if settings.TEMPLATE_DEBUG:
            raise
        else:
            yield []
