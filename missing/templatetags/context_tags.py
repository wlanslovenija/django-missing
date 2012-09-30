from django import template
from django.conf import settings

register = template.Library()

class SetContextNode(template.Node):
    def __init__(self, nodelist, variable):
        self.nodelist = nodelist
        self.variable = variable
    
    def render(self, context):
        try:
            context[self.variable] = self.nodelist.render(context)
        except:
            if settings.TEMPLATE_DEBUG:
                raise
        return u''

@register.tag
def setcontext(parser, token):
    """
    Sets (updates) current template context with the rendered output of the block inside tags.

    This is useful when some template tag does not support storing its output in the context itself or we need some complex content (like language, user or URL dependent content) multiple times.

    Example usage::

        {% setcontext as varname %}
            {% complextag %}
        {% endsetcontext %}
    """
    nodelist = parser.parse(('endsetcontext',))
    args = list(token.split_contents())
    
    if len(args) != 3 or args[1] != "as":
        raise template.TemplateSyntaxError("'%s' expected format is 'as name'" % args[0])
    variable = args[2]
    
    parser.delete_first_token()
    
    return SetContextNode(nodelist, variable)
