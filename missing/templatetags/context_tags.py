from django import template
from django.conf import settings

register = template.Library()

# We extend TextNode so that it can be used before {% extend %}
class SetContextNode(template.TextNode):
    def __init__(self, nodelist, variable=None):
        super(SetContextNode, self).__init__(u'')
        self.nodelist = nodelist
        self.variable = variable

    def __repr__(self):
        return super(template.TextNode, super(SetContextNode, self)).__repr__()

    def render(self, context):
        try:
            output = self.nodelist.render(context)
            if self.variable:
                context[self.variable] = output
        except:
            if settings.TEMPLATE_DEBUG:
                raise

        return super(SetContextNode, self).render(context)

@register.tag
def setcontext(parser, token):
    """
    Sets (updates) current template context with the rendered output of the block inside tags.

    This is useful when some template tag does not support storing its output in the context itself
    or we need some complex content (like language, user or URL dependent content) multiple times.

    Variable name is optional. If not given, output is discarded. This is useful when you are interested
    just in side-effects, like modifying template context. Because the tag can be used before :tag:`extend` tag
    you can use it to modify context of an extended template and be sure it is set before any :tag:`block`
    is rendered.

    Example usage::

        {% setcontext as varname %}
            {% complextag %}
        {% endsetcontext %}
    """

    nodelist = parser.parse(('endsetcontext',))
    args = list(token.split_contents())

    if len(args) == 1:
        variable = None
    else:
        if len(args) != 3 or args[1] != "as":
            raise template.TemplateSyntaxError("'%s' tag takes none or 2 arguments and the first argument must be 'as'" % args[0])
        variable = args[2]

    parser.delete_first_token()
    
    return SetContextNode(nodelist, variable)
