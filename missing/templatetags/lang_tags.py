from django import template
from django.conf import settings
from django.utils import encoding, translation

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
        translated = encoding.force_text(translation.ugettext(string))
        translation.activate(old_lang)
        return translated
    except:
        if settings.DEBUG:
            raise
        return u''
