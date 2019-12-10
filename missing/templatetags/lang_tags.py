from django import template
from django.conf import settings
from django.utils import translation
# Remove this check when support for Python 2 is dropped.
# https://docs.djangoproject.com/en/3.0/releases/3.0/#django-utils-encoding-force-text-and-smart-text
import sys
if sys.version_info[0] >= 3:
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str

register = template.Library()

@register.simple_tag
def translate(string, lang_code):
    """
    Translates given string to the specified language.

    This is useful for text you need in some other language than the current language. For example,
    for links inviting users to switch to their language.

    Example usage::

        {% translate "Do you understand this?" "de" %}
    """

    try:
        old_lang = translation.get_language()
        translation.activate(lang_code)
        translated = force_str(translation.ugettext(string))
        translation.activate(old_lang)
        return translated
    except:
        if settings.DEBUG:
            raise
        return u''
