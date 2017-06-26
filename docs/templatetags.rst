Template Tags and Filters
=========================

``context_tags`` module
-----------------------

You need to add ``missing.templatetags.context_tags`` to your ``builtins`` option
for the ``DjangoTemplates`` backend to be able to use these tags immediately after
``extends`` tag.

.. automodule:: missing.templatetags.context_tags
    :members:

``forloop_tags`` module
-----------------------

Use ``{% load forloop_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.forloop_tags
    :members:

``html_tags`` module
--------------------

Use ``{% load html_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.html_tags
    :members:

``lang_tags`` module
--------------------

Use ``{% load lang_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.lang_tags
    :members:

``list_tags`` module
--------------------

Use ``{% load list_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.list_tags
    :members:

``string_tags`` module
----------------------

Use ``{% load string_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.string_tags
    :members:

``url_tags`` module
-------------------

Use ``{% load url_tags %}`` in your template to load this module.

.. automodule:: missing.templatetags.url_tags
    :members:
