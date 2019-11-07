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

@register.filter
def count(value, arg):
    """
    Returns the number of non-overlapping occurrences of an argument substring in the given string.
    """

    return value.count(arg)

@register.filter
def startswith(value, arg):
    """
    Returns True if the given string starts with an argument prefix, otherwise returns False.
    """

    return value.startswith(arg)

@register.filter
def endswith(value, arg):
    """
    Returns True if the given string ends with an argument suffix, otherwise returns False.
    """

    return value.endswith(arg)
