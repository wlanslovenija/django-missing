from django.contrib.admindocs import utils

DUMMY_ROLES = (
    'py:meth',
    'py:func',
)

def dummy_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    if options is None:
        options = {}
    if content is None:
        content = []
    node = docutils.nodes.literal(rawtext, text, **options)
    return [node], []

if utils.docutils_is_available:
    import docutils

    for role in DUMMY_ROLES:
        docutils.parsers.rst.roles.register_canonical_role(role, dummy_role)
