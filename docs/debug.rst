Debugging
=========

Safer ExceptionReporterFilter
-----------------------------

.. automodule:: missing.debug
    :members:

Non-silent NoReverseMatch
-------------------------

``NoReverseMatch`` is by default a silent exception in variables, its output replaced by ``TEMPLATE_STRING_IF_INVALID``
setting. Sometimes you want a bit more loud expression of mismatched URL reversing, so you can set
``URL_RESOLVERS_DEBUG`` to ``True`` to normally raise an exception. Only active when ``DEBUG`` is set
to ``True`` as well.
