import math

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def split_list(value, length):
    """
    Splits input list into sublists of the given length.
    
    Last sublist can be shorter if input list length is not a multiplier of the given length.

    Example usage::

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
        if settings.DEBUG:
            raise
        else:
            yield []

@register.filter
def divide_list(value, count):
    """
    Divides input list into the given number of sublists.
    
    Last sublist can be shorter if input list length is not a multiplier of the given number of sublists.

    Example usage::

        <tr>
        {% for column in objects|divide_list:"2" %}
            <td><ul>
            {% for obj in column %}
                <li>{{ obj }}</li>
            {% endfor %}
            </ul></td>
        {% endfor %}
        </tr>
    """

    try:
        value = list(value)
        count = int(count)

        if not count:
            yield value
            return

        new_len = int(1.0 * len(value) / count + 0.5)
        for i in xrange(0, count-1):
             yield value[i*new_len:(i+1)*new_len]
        yield value[count*new_len-new_len:]
    except:
        if settings.DEBUG:
            raise
        else:
            yield []
