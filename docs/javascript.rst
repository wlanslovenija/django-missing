JavaScript Functions
====================

Automatic Slug Generation
-------------------------

Django admin and other Django applications can have slug fields which are automatically updated/generated in user's browser using JavaScript. Django bundles JavaScript code necessary for this but it behaves differently than built-in :filter:`slugify` template filter in Python. For this reason django-missing provides JavaScript code with equal functionality, implemented directly in JavaScript. It comes in two flavors:

``slugify`` equivalent
``````````````````````

A JavaScript equivalent to built-in :filter:`slugify` template filter. You can load by adding something like this in your page (or Django admin) ``<head>`` section (in template)::

    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/n11ndata.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/n11n.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/urlify.js"></script>

Of course above mentioned files should be `published by your Django site installation`_.

.. _published by your Django site installation: https://docs.djangoproject.com/en/dev/howto/static-files/

``slugify2`` equivalent
```````````````````````

If you want to use improved :py:func:`~missing.templatetags.url_tags.slugify2` template filter in Python, you can also use its equivalent in JavaScript::

    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/n11ndata.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/n11n.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL|default:MEDIA_URL }}missing/urlify2.js"></script>
