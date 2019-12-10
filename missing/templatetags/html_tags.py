from __future__ import absolute_import

from django import template
from django.conf import settings
# Remove this check when support for Python < 3.4 is dropped.
# https://docs.djangoproject.com/en/3.0/releases/3.0/#id3
try:
    from html import unescape
except ImportError:
    from django.utils.text import unescape_entities as unescape
# Remove this check when support for Python 2 is dropped.
# https://docs.djangoproject.com/en/3.0/releases/3.0/#django-utils-encoding-force-text-and-smart-text
import sys
if sys.version_info[0] >= 3:
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str

from . import url_tags

register = template.Library()

@register.filter
def anchorify(anchor):
    """
    Filter which converts to a string suitable for use as an anchor id on a HTML element.

    This is useful when you want anchor id on a heading to match heading content, which can
    be an arbitrary string.

    Example usage::

        <h1 id="{{ _("My Blog")|anchorify }}">{% trans "My Blog" %}</h1>

    The result would be::

        <h1 id="my-blog">My Blog</h1>
    """

    try:
        anchor = template.defaultfilters.striptags(anchor)
        anchor = unescape(anchor)
        anchor = url_tags.slugify2(anchor)
        if not anchor or not anchor[0].isalpha():
            anchor = 'a' + anchor
        return anchor
    except:
        if settings.DEBUG:
            raise
        else:
            return u''

@register.inclusion_tag(('heading.html', 'missing/heading.html'), takes_context=True)
def heading(context, level, content, classes=''):
    """
    Renders heading with unique anchor id using a template.

    Tag assures that each anchor id is unique inside the whole rendered template where it is used.
    Of course, only for headings created with the tag.

    Heading level will be adjusted based on base heading level set by
    :py:func:`~missing.templatetags.html_tags.set_base_heading_level` or ``base_heading_level`` context
    variable. This is useful if you have
    some static main ``<h1>`` with a site name and you want other headings to have a higher level
    automatically, but you want to reuse the same template you use can independently, without site
    name heading.
    Or if you include same template which uses this tag at various places where different
    heading level is needed based on the existing heading nesting. By default base heading level is
    0, so no adjustment will be made, so example below will make a ``<h1>`` heading.

    Optionally you can pass CSS classes string which will be passed through to the heading template.
    It uses ``heading.html`` or ``missing/heading.html`` template.

    Example usage::

        {% heading 1 _("My Blog") %}

    The result would be::

        <h1 id="my-blog" class="heading ">My Blog</h1>
    """

    anchor = base_anchor = anchorify(content)

    # We fetch top level render context to make sure anchors are
    # unique inside the whole template, not just inside the current
    # render context
    top_render_context = context.render_context.dicts[0]

    i = 0
    while anchor in top_render_context.setdefault('heading_anchors', {}):
        anchor = base_anchor + "-" + force_str(i)
        i += 1
    top_render_context['heading_anchors'][anchor] = True

    return {
        'level': context.get('base_heading_level', 0) + level,
        'content': content,
        'id': anchor,
        'classes': classes,
    }

@register.simple_tag(takes_context=True)
def set_base_heading_level(context, level, top_level=False):
    """
    Set base heading level to a given numeric level to adjust heading levels
    of headings created by the :py:func:`~missing.templatetags.html_tags.heading` tag.

    You can also set base heading level by setting ``base_heading_level`` context
    variable. For example, by using built-in :tag:`with` tag.

    If you set ``top_level`` to ``True``, base heading level will be set at the top
    context level for the whole template. This is useful if you want to set base heading
    level for the whole template, but you are using the tag somewhere nested in blocks and
    includes. It will set base heading level only at the top context level so if you set
    heading level explicitly at some other context levels as well they will still take
    precedence.

    Example usage::

        {% set_base_heading_level 1 %}
        {% heading 1 _("My Blog") %}

    The result would be::

        <h2 id="my-blog" class="heading ">My Blog</h2>
    """

    if top_level:
        # For Django > 1.4 an empty context contains already builtins, so depending
        # on that fact we set `base_heading_level` at the appropriate level.
        if template.Context().dicts == [{}]:
            top_level_index = 0
        else:
            top_level_index = 1

        # Ugly way of accessing top level context directly.
        context.dicts[top_level_index]['base_heading_level'] = level
    else:
        context['base_heading_level'] = level

    # Return nothing
    return u''
