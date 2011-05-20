from django import template

register = template.Library()

@register.tag
def fullurl(parser, token):
    args = list(token.split_contents())

    if len(args) != 2:
        raise template.TemplateSyntaxError("'%s' tag requires exactly one argument" % args[0])

    url = parser.compile_filter(args[1])
    return FullUrlNode(url)

class FullUrlNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        try:
            return context['request'].build_absolute_uri(self.url.resolve(context))
        except:
            return u''
