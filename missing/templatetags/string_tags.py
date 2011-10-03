import re

from django import template
from django.template import defaultfilters

register = template.Library()

@register.filter
@defaultfilters.stringfilter
def ensure_sentence(value):
    """
    Ensures that string ends with dot if it does not already end with some punctuation.
    """

    value = value.rstrip()
    if value and value[-1] not in ".?!,;)":
        return u"%s." % (value,)
    return value
