JavaScript
==========

Automatic Slug Generation
-------------------------

Django admin and other Django applications can have slug fields which are automatically updated/generated in user's browser using JavaScript. Django bundles JavaScript code necessary for this but it behaves differently than built-in :filter:`slugify` template filter in Python. For this reason django-missing provides JavaScript code with equal functionality, implemented directly in JavaScript. It comes in two flavors:

``slugify`` equivalent
``````````````````````

A JavaScript equivalent to built-in :filter:`slugify` template filter. You can load by adding something like this in your page (or Django admin) ``<head>`` section (in template)::

    <script type="text/javascript" src="{{ STATIC_URL }}missing/n11ndata.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}missing/n11n.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}missing/urlify.js"></script>

Of course above mentioned files should be `published by your Django site installation`_.

.. _published by your Django site installation: https://docs.djangoproject.com/en/dev/howto/static-files/

``slugify2`` equivalent
```````````````````````

If you want to use improved :py:func:`~missing.templatetags.url_tags.slugify2` template filter in Python, you can also use its equivalent in JavaScript::

    <script type="text/javascript" src="{{ STATIC_URL }}missing/n11ndata.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}missing/n11n.js"></script>
    <script type="text/javascript" src="{{ STATIC_URL }}missing/urlify2.js"></script>

Datetime Formatting
-------------------

Once you load `internationalization in JavaScript code`_, Django provides ``get_format`` function to access
configured `datetime and other formats`_ but it is lacking function to format JavaScript ``Date`` objects
according to those formats. By loading::

    <script type="text/javascript" src="{{ STATIC_URL }}missing/date.js"></script>

JavaScript ``Date`` prototype is extended with ``strfdate`` method::

    new Date().strfdate(get_format('DATETIME_FORMAT'))

Note, to format datetime input formats (those using ``%`` for placeholders) Django admin provides limited support
through its ``strftime`` method added to JavaScript ``Date`` prototype when loading::

    <script type="text/javascript" src="{{ STATIC_URL }}admin/js/core.js"></script>

and use, for example, as::

    new Date().strftime(get_format('DATE_INPUT_FORMATS')[0])

.. _internationalization in JavaScript code: https://docs.djangoproject.com/en/dev/topics/i18n/translation/#internationalization-in-javascript-code
.. _datetime and other formats: https://docs.djangoproject.com/en/dev/topics/i18n/formatting/

Relative datetime
-----------------

JavaScript implementations of :filter:`timesince`, :filter:`timeuntil`, and :filter:`naturaltime` Django filters
are also available as extensions to JavaScript ``Date`` prototype by loading::

    <script type="text/javascript" src="{{ STATIC_URL }}missing/humanize.js"></script>

Additionally, ``updatingNaturaltime`` method is provided which behaves similarly to ``naturaltime`` method but
it takes a DOM element or jQuery selector as an optional argument and makes sure it is updated as time progresses.
