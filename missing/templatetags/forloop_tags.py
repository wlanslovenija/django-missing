from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def css_classes(context, first, last, odd, even):
    """
    Maps loop variables of :tag:`for` tag to CSS classes string.

    Takes names of first, last, odd, even CSS classes, respectively

    Example usage::

        {% css_classes "first" "last" "odd" "even" %}
    """

    classes = []
    if context['forloop'].get('first', False):
        classes.append(first)
    if context['forloop'].get('last', False):
        classes.append(last)
    if context['forloop']['revcounter'] % 2 == 1:
        classes.append(odd)
    else:
        classes.append(even)

    return u' '.join(classes)
