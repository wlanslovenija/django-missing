from django.template import base, loader

# To load docutils extensions somewhere
from missing import admindocs

# To be able to use "setcontext" tag before "extends" tag, we add it to built-in tags
loader.add_to_builtins('missing.templatetags.context_tags')

# Monkey-patch Django template Parser to make all text nodes before "extends" tag empty
if not getattr(base.Parser, '_django_missing_extended', False):
    original_extend_nodelist = base.Parser.extend_nodelist

    def extend_nodelist(self, nodelist, node, token):
        original_extend_nodelist(self, nodelist, node, token)

        if node.must_be_first and len(nodelist) > 1:
            # Node must be first and there was no exception, so nodes
            # before are all TextNode instances
            for n in nodelist[:-1]: # Except the last one, which is current node
                n.s = u''

    base.Parser.extend_nodelist = extend_nodelist
