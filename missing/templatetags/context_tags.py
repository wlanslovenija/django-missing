from django.conf import settings

# We have to import "loader" first to prevent import cycle issues when building documentation
from django import template
from django.template import loader, loader_tags, base

CONTEXT_BLOCK_NAME = '__context_block__'

register = template.Library()


class SetContextNode(base.Node):
    def __init__(self, nodelist, variable):
        self.nodelist = nodelist
        self.variable = variable

    def render(self, context):
        try:
            context[self.variable] = self.nodelist.render(context)
        except:
            if settings.DEBUG:
                raise

        return u''


@register.tag
def setcontext(parser, token):
    """
    Sets (updates) current template context with the rendered output of the block inside tags.

    This is useful when some template tag does not support storing its output in the context itself
    or we need some complex content (like language, user or URL dependent content) multiple times.

    Example usage::

        {% setcontext as varname %}
            {% complextag %}
        {% endsetcontext %}
    """

    nodelist = parser.parse(('endsetcontext',))
    args = list(token.split_contents())

    if len(args) != 3 or args[1] != "as":
        raise base.TemplateSyntaxError("'%s' tag takes 2 arguments and the first argument must be 'as'" % args[0])
    variable = args[2]

    parser.delete_first_token()

    return SetContextNode(nodelist, variable)


class ContextBlockNode(loader_tags.BlockNode):
    # We want it to be the first tag in the template
    must_be_first = True

    def __init__(self, name, nodelist):
        super(ContextBlockNode, self).__init__(CONTEXT_BLOCK_NAME, nodelist)

    # Copy of BlockNode.render which does not push and pop context around the
    # block so that block rendering can modify current context
    def _render(self, context):
        block_context = context.render_context.get(loader_tags.BLOCK_CONTEXT_KEY)
        if block_context is None:
            context['block'] = self
            result = self.nodelist.render(context)
        else:
            push = block = block_context.pop(self.name)
            if block is None:
                block = self
            # Create new block so we can store context without thread-safety issues.
            block = type(self)(block.name, block.nodelist)
            block.context = context
            context['block'] = block
            result = block.nodelist.render(context)
            if push is not None:
                block_context.push(self.name, push)
        return result

    def render(self, context):
        try:
            # We ignore the output
            self._render(context)
        except:
            if settings.DEBUG:
                raise
        return u''

    def super(self):
        if not hasattr(self, 'context'):
            return u''

        super(ContextBlockNode, self).super()

        # We make sure block.super is called only once
        render_context = self.context.render_context
        if (loader_tags.BLOCK_CONTEXT_KEY in render_context and render_context[loader_tags.BLOCK_CONTEXT_KEY].get_block(self.name) is not None):
            render_context[loader_tags.BLOCK_CONTEXT_KEY].pop(self.name)

        return u''


@register.tag
def contextblock(parser, token):
    """
    A special :tag:`block` tag which does not render anything but can be used to modify a template
    context.

    The tag is rendered first thus modifying context before other blocks are rendered. A tag in an
    extending template is rendered after parent tags, allowing you to override template context in
    child templates.

    The tag has to be the first tag, immediately after the :tag:`extends` tag. You have to define
    a empty context block tag at the very start of your base template.

    Example usage, in your base template::

        {% contextblock %}{% endcontextblock %}<html>
            <body>
                <head>
                    <title>{{ title }}</title>
                </head>
                <body>
                    <h1>{{ title }}</h1>
                    <p><a href="{{ homepage }}">{{ title }}</a></p>
                </body>
            </body>
        </html>

    In your extending template::

        {% extends "base.html" %}

        {% contextblock %}
            {% load future i18n %}
            {% setcontext as title %}{% blocktrans %}{{ username }}'s blog{% endblocktrans %}{% endsetcontext %}
            {% url "homepage" as homepage %}
        {% endcontextblock %}
    """

    nodelist = parser.parse(('endcontextblock',))

    if hasattr(base, 'TokenType'):
        TOKEN_VAR = base.TokenType.VAR
    else:
        TOKEN_VAR = base.TOKEN_VAR

    # Make sure we call block.super at least once
    # (and in ContextBlockNode.super we make sure it is called only once)
    block_super_token = base.Token(TOKEN_VAR, 'block.super')
    if hasattr(token, 'source'):
        block_super_token.source = token.source
    filter_expression = parser.compile_filter(block_super_token.contents)
    var_node = base.VariableNode(filter_expression)
    # To push it through the normal logic first
    parser.extend_nodelist(nodelist, var_node, block_super_token)
    # But we want it at the very beginning
    var_node = nodelist.pop()
    nodelist.insert(0, var_node)

    parser.delete_first_token()

    return ContextBlockNode(None, nodelist)
