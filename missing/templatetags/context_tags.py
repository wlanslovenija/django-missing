from django import template

register = template.Library()

class SetContextNode(template.Node):
    """
    This class defines renderer which just updates current template context with the rendered output of the block inside tags.
    """
    def __init__(self, nodelist, variable):
        self.nodelist = nodelist
        self.variable = variable
    
    def render(self, context):
        context[self.variable] = self.nodelist.render(context)
        return ''

@register.tag
def setcontext(parser, token):
    """
    Sets (updates) current template context with the rendered output of the block inside tags.
    """
    nodelist = parser.parse(('endsetcontext',))
    args = list(token.split_contents())
    
    if len(args) != 3 or args[1] != "as":
        raise TemplateSyntaxError("%r expected format is 'as name'" % args[0])
    variable = args[2]
    
    parser.delete_first_token()
    
    return SetContextNode(nodelist, variable)
