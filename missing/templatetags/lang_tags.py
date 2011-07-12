from django import template
from django.utils import translation

register = template.Library()

@register.simple_tag
def translate(string, lang_code):
    old_lang = translation.get_language()
    translation.activate(lang_code)
    translated = unicode(translation.ugettext(string))
    translation.activate(old_lang)
    return translated
