from django.template import loader

# To load docutils extensions somewhere
from missing import admindocs

# To be able to use "setcontext" tag before "extends" tag, we add it to built-in tags
loader.add_to_builtins('missing.templatetags.context_tags')
