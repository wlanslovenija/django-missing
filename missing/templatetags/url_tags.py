# -*- coding: utf-8 -*-

import re, unicodedata

from django import template
try:
    from django import urls
except ImportError:
    from django.core import urlresolvers as urls
from django.conf import settings
from django.template import defaultfilters
from django.utils import html, safestring
# Remove this check when support for Python 2 is dropped.
# https://docs.djangoproject.com/en/3.0/releases/3.0/#django-utils-encoding-force-text-and-smart-text
import sys
if sys.version_info[0] >= 3:
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str

register = template.Library()

class FullUrlNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        try:
            location = None
            if self.url:
                location = self.url.resolve(context)
            return context['request'].build_absolute_uri(location)
        except:
            if settings.DEBUG:
                raise
            return u''

@register.tag
def fullurl(parser, token):
    """
    Builds an absolute (full) URL from the given location and the variables available in the request.

    If no location is specified, the absolute (full) URL is built on :py:meth:`django.http.HttpRequest.get_full_path`.

    It is a wrapper around :py:meth:`django.http.HttpRequest.build_absolute_uri`. It requires ``request`` to be available
    in the template context (for example, by using ``django.core.context_processors.request`` context processor).

    Example usage::

        {% url "view_name" as the_url %}
        {% fullurl the_url %}
    """

    args = list(token.split_contents())

    if len(args) > 2:
        raise template.TemplateSyntaxError("'%s' tag requires at most one argument" % args[0])

    if len(args) == 2:
        url = parser.compile_filter(args[1])
    else:
        url = None

    return FullUrlNode(url)

DASH_START_END_RE = re.compile(r'^-+|-+$')

LATIN_MAP = {
    'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'Ç':
    'C', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I',
    'Ï': 'I', 'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö':
    'O', 'Ő': 'O', 'Ø': 'O', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ű': 'U',
    'Ý': 'Y', 'Þ': 'TH', 'ß': 'ss', 'à':'a', 'á':'a', 'â': 'a', 'ã': 'a', 'ä':
    'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ð': 'd', 'ñ': 'n', 'ò': 'o', 'ó':
    'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ő': 'o', 'ø': 'o', 'ù': 'u', 'ú': 'u',
    'û': 'u', 'ü': 'u', 'ű': 'u', 'ý': 'y', 'þ': 'th', 'ÿ': 'y'
}
LATIN_SYMBOLS_MAP = {
    '©':'(c)'
}
GREEK_MAP = {
    'α':'a', 'β':'b', 'γ':'g', 'δ':'d', 'ε':'e', 'ζ':'z', 'η':'h', 'θ':'8',
    'ι':'i', 'κ':'k', 'λ':'l', 'μ':'m', 'ν':'n', 'ξ':'3', 'ο':'o', 'π':'p',
    'ρ':'r', 'σ':'s', 'τ':'t', 'υ':'y', 'φ':'f', 'χ':'x', 'ψ':'ps', 'ω':'w',
    'ά':'a', 'έ':'e', 'ί':'i', 'ό':'o', 'ύ':'y', 'ή':'h', 'ώ':'w', 'ς':'s',
    'ϊ':'i', 'ΰ':'y', 'ϋ':'y', 'ΐ':'i',
    'Α':'A', 'Β':'B', 'Γ':'G', 'Δ':'D', 'Ε':'E', 'Ζ':'Z', 'Η':'H', 'Θ':'8',
    'Ι':'I', 'Κ':'K', 'Λ':'L', 'Μ':'M', 'Ν':'N', 'Ξ':'3', 'Ο':'O', 'Π':'P',
    'Ρ':'R', 'Σ':'S', 'Τ':'T', 'Υ':'Y', 'Φ':'F', 'Χ':'X', 'Ψ':'PS', 'Ω':'W',
    'Ά':'A', 'Έ':'E', 'Ί':'I', 'Ό':'O', 'Ύ':'Y', 'Ή':'H', 'Ώ':'W', 'Ϊ':'I',
    'Ϋ':'Y'
}
TURKISH_MAP = {
    'ş':'s', 'Ş':'S', 'ı':'i', 'İ':'I', 'ç':'c', 'Ç':'C', 'ü':'u', 'Ü':'U',
    'ö':'o', 'Ö':'O', 'ğ':'g', 'Ğ':'G'
}
RUSSIAN_MAP = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'yo', 'ж':'zh',
    'з':'z', 'и':'i', 'й':'j', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o',
    'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'h', 'ц':'c',
    'ч':'ch', 'ш':'sh', 'щ':'sh', 'ъ':'', 'ы':'y', 'ь':'', 'э':'e', 'ю':'yu',
    'я':'ya',
    'А':'A', 'Б':'B', 'В':'V', 'Г':'G', 'Д':'D', 'Е':'E', 'Ё':'Yo', 'Ж':'Zh',
    'З':'Z', 'И':'I', 'Й':'J', 'К':'K', 'Л':'L', 'М':'M', 'Н':'N', 'О':'O',
    'П':'P', 'Р':'R', 'С':'S', 'Т':'T', 'У':'U', 'Ф':'F', 'Х':'H', 'Ц':'C',
    'Ч':'Ch', 'Ш':'Sh', 'Щ':'Sh', 'Ъ':'', 'Ы':'Y', 'Ь':'', 'Э':'E', 'Ю':'Yu',
    'Я':'Ya'
}
UKRAINIAN_MAP = {
    'Є':'Ye', 'І':'I', 'Ї':'Yi', 'Ґ':'G', 'є':'ye', 'і':'i', 'ї':'yi', 'ґ':'g'
}
CZECH_MAP = {
    'č':'c', 'ď':'d', 'ě':'e', 'ň': 'n', 'ř':'r', 'š':'s', 'ť':'t', 'ů':'u',
    'ž':'z', 'Č':'C', 'Ď':'D', 'Ě':'E', 'Ň': 'N', 'Ř':'R', 'Š':'S', 'Ť':'T',
    'Ů':'U', 'Ž':'Z'
}
POLISH_MAP = {
    'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z',
    'ż':'z', 'Ą':'A', 'Ć':'C', 'Ę':'e', 'Ł':'L', 'Ń':'N', 'Ó':'o', 'Ś':'S',
    'Ź':'Z', 'Ż':'Z'
}
LATVIAN_MAP = {
    'ā':'a', 'č':'c', 'ē':'e', 'ģ':'g', 'ī':'i', 'ķ':'k', 'ļ':'l', 'ņ':'n',
    'š':'s', 'ū':'u', 'ž':'z', 'Ā':'A', 'Č':'C', 'Ē':'E', 'Ģ':'G', 'Ī':'i',
    'Ķ':'k', 'Ļ':'L', 'Ņ':'N', 'Š':'S', 'Ū':'u', 'Ž':'Z'
}
LITHUANIAN_MAP = {
    'ą':'a', 'č':'c', 'ę':'e', 'ė':'e', 'į':'i', 'š':'s', 'ų':'u', 'ū':'u',
    'ž':'z', 'Ą':'A', 'Č':'C', 'Ę':'E', 'Ė':'E', 'Į':'I', 'Š':'S', 'Ų':'U',
    'Ū':'U', 'Ž':'Z'
}
SERBIAN_MAP = {
    'ђ': 'dj', 'ј' : 'j', 'љ' : 'lj', 'њ' : 'nj', 'ћ': 'c', 'џ': 'dz', 'đ' : 'dj',
    'Ђ' : 'Dj', 'Ј' : 'j', 'Љ' : 'Lj', 'Њ' : 'Nj', 'Ћ' : 'C', 'Џ' : 'Dz', 'Đ' : 'Dj'
}

ALL_DOWNCODE_MAPS = [
    LATIN_MAP,
    LATIN_SYMBOLS_MAP,
    GREEK_MAP,
    TURKISH_MAP,
    RUSSIAN_MAP,
    UKRAINIAN_MAP,
    CZECH_MAP,
    POLISH_MAP,
    LATVIAN_MAP,
    LITHUANIAN_MAP,
    SERBIAN_MAP
]

class Downcoder(object):
    map = {}
    regex = None

    def __init__(self):
        self.map = {}
        chars = u''

        for lookup in ALL_DOWNCODE_MAPS:
            for c, l in lookup.items():
                c = unicodedata.normalize('NFC', force_str(c))
                l = force_str(l.encode('ascii', 'strict'), encoding='ascii')
                self.map[c] = l
                chars += c

        self.regex = re.compile(r'[' + chars + ']|[^' + chars + ']+', re.U)

downcoder = Downcoder()

def downcode(value):
    downcoded = u''
    pieces = downcoder.regex.findall(value)

    if pieces:
        for p in pieces:
            mapped = downcoder.map.get(p)
            if mapped:
                downcoded += mapped
            else:
                downcoded += p
    else:
        downcoded = value

    return downcoded

@register.filter(is_safe=True)
@defaultfilters.stringfilter
def slugify2(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    It is similar to built-in :filter:`slugify` but it also handles special characters in variety of languages
    so that they are not simply removed but properly transliterated/downcoded.
    """

    try:
        value = unicodedata.normalize('NFC', value)
        value = downcode(value)
        value = force_str(unicodedata.normalize('NFD', value).encode('ascii', 'ignore'), encoding='ascii')
        value = force_str(re.sub(r'[^\w\s-]', '', value).strip().lower())
        value = re.sub(r'[-\s]+', '-', value)
        value = DASH_START_END_RE.sub('', value)
        return safestring.mark_safe(value)
    except:
        if settings.DEBUG:
            raise
        else:
            return u''

def unnamed_group_name(param):
    # Converts unnamed groups sequence numbers prefixed with _ to just numbers
    if param.startswith('_') and param[1:].isdigit():
        return param[1:]
    else:
        return param

def urltemplate_with_prefix(resolver, view, prefix, *args, **kwargs):
    if args and kwargs:
        raise ValueError("Don't mix *args and **kwargs.")
    elif args:
        args = list(args)

    possibilities = resolver.reverse_dict.getlist(view)

    for possibility_entry in possibilities:
        if len(possibility_entry) == 3:
            possibility, pattern, defaults = possibility_entry
        else:
            possibility, pattern, defaults, converters = possibility_entry

        assert len(possibility) > 0

        if len(possibility) > 1:
            raise NotImplementedError

        result, params = possibility[0]

        if kwargs and len(set(kwargs.keys()) - set(params)):
            # Not all given pre-filled values exist in this URL pattern
            continue

        if args and len(params) < len(args):
            # Too many pre-filled values for this URL pattern
            continue

        if args:
            for i, param in enumerate(params):
                if i < len(args):
                    result = result.replace('%%(%s)s' % param, force_str(args[i]))
                else:
                    result = result.replace('%%(%s)s' % param, '{%s}' % unnamed_group_name(param))
        else:
            for param in params:
                result = result.replace('%%(%s)s' % param, force_str(kwargs.get(param, '{%s}' % unnamed_group_name(param))))

        return prefix + result

    raise urls.NoReverseMatch("Reverse for '%s' with arguments '%s' and keyword arguments '%s' not found." % (view, args, kwargs))

def urltemplate_namespaces(viewname, current_app=None, *args, **kwargs):
    urlconf = urls.get_urlconf()
    resolver = urls.get_resolver(urlconf)
    prefix = urls.get_script_prefix()

    parts = viewname.split(':')
    parts.reverse()
    view = parts[0]
    path = parts[1:]

    resolved_path = []
    ns_pattern = ''
    while path:
        ns = path.pop()

        # Lookup the name to see if it could be an app identifier
        try:
            app_list = resolver.app_dict[ns]
            # Yes! Path part matches an app in the current Resolver
            if current_app and current_app in app_list:
                # If we are reversing for a particular app,
                # use that namespace
                ns = current_app
            elif ns not in app_list:
                # The name isn't shared by one of the instances
                # (i.e., the default) so just pick the first instance
                # as the default.
                ns = app_list[0]
        except KeyError:
            pass

        try:
            extra, resolver = resolver.namespace_dict[ns]
            resolved_path.append(ns)
            ns_pattern = ns_pattern + extra
        except KeyError as key:
            if resolved_path:
                raise urls.NoReverseMatch("%s is not a registered namespace inside '%s'" % (key, ':'.join(resolved_path)))
            else:
                raise urls.NoReverseMatch("%s is not a registered namespace" % key)
    if ns_pattern:
        resolver = urls.get_ns_resolver(ns_pattern, resolver)

    return urltemplate_with_prefix(resolver, view, prefix, *args, **kwargs)

@register.simple_tag(takes_context=True)
def urltemplate(context, viewname, *args, **kwargs):
    """
    Creates URI template in a similar way to how ``url`` tags work but leaving parts of
    a URI to be filled in by a client. See :rfc:`6570` for more information.

    Names of parts are taken from named groups in URL regex pattern used for the view,
    or as a part's sequence number (zero-based) for unnamed groups. You can pre-fill
    some parts by specifying them as additional arguments to the tag.

    .. warning:: Tag cannot check if pre-fill values specified will really match back
                 the URL regex pattern, so make sure yourself that they do.

    Example usage::

        {% with variable="42" %}
            {% urltemplate "view_name" arg1="value" arg2=variable %}
        {% endwith %}

    If URL pattern would be defined like::

        url(r'^some/view/(?P<arg1>.*)/(?P<arg2>.*)/(?P<param>.*)/$', some_view, name='view_name'),

    The result would be::

        /some/view/value/42/{param}/
    """

    try:
        try:
            current_app = context.current_app
        except AttributeError:
            try:
                current_app = context.request.current_app
            except AttributeError:
                try:
                    current_app = context.request.resolver_match.namespace
                except AttributeError:
                    current_app = None

        url = urltemplate_namespaces(viewname, current_app, *args, **kwargs)
        if context.autoescape:
            url = html.conditional_escape(url)
        return safestring.mark_safe(url)
    except:
        if settings.DEBUG:
            raise
        else:
            return u''

@register.simple_tag(takes_context=True)
def active_url(context, urls, class_name='active'):
    """
    Returns ``class_name`` (default ``active``) if any of given ``urls`` are real prefixes
    of the current request path.

    Useful when you want to highlight links to the current section of the site. For example,
    in menu entries.

    Example usage::

        {% active_url "/test/" %}
    """

    if not urls:
        return u''

    if not hasattr(urls, '__iter__'):
        urls = [urls]

    try:
        for url in urls:
            # To make sure we use resolved lazy instances,
            # otherwise there are sometimes errors
            url = force_str(url)

            if not url:
                continue

            if url.startswith('/'):
                current_url = context['request'].path
            else:
                current_url = context['request'].build_absolute_uri(context['request'].path)

            if url == current_url:
                return class_name

            if url == '/':
                # If url is / it would match anything
                # It should be true only if current_url is /,
                # which we tested already above
                continue

            # True if url is a real prefix of current_url
            # We test for equality above, so if it is a prefix
            # then current_url is for sure longer, so we test
            # that prefix ends with /, to make sure it is a real
            # path prefix
            if current_url.startswith(url) and current_url.startswith('%s/' % url):
                return class_name

        return u''
    except:
        if settings.DEBUG:
            raise
        else:
            return u''
