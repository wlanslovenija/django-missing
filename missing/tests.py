# -*- coding: utf-8 -*-

from django import template
from django import test
from django.test import client

class ContextTagsTest(test.TestCase):
    def test_setcontext_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load context_tags %}
            {% setcontext %}
            FooBar
            {% endsetcontext %}
            """)

        self.assertIn('expected format', str(cm.exception))

    def test_setcontext_2(self):
        t = template.Template("""
        {% load context_tags %}
        {% setcontext as variable %}
        FooBar
        {% endsetcontext %}
        """)
        c = template.Context()
        o = t.render(c).strip()
       
        self.assertIn('variable', c)
        self.assertEquals(c['variable'].strip(), 'FooBar')
        self.assertEquals(o, '')

class LangTagsTest(test.TestCase):
    def test_translate_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load lang_tags %}
            {% translate "FooBar" %}
            """)

        self.assertEquals('translate takes 2 arguments', str(cm.exception))

class ListTagsTest(test.TestCase):
    def test_split_list_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load list_tags %}
            {{ objects|split_list }}
            """)

        self.assertEquals('split_list requires 1 arguments, 0 provided', str(cm.exception))

    def test_split_list_2(self):
        t = template.Template("""
        {% load list_tags %}
        |{% for group in objects|split_list:"4" %}{{ group|length }}|{% endfor %}
        """)
        c = template.Context({
            'objects': range(10),
        })
        o = t.render(c).strip()
       
        self.assertEquals(o, '|4|4|2|')

    def test_split_list_3(self):
        t = template.Template("""
        {% load list_tags %}
        {% for group in objects|split_list:"5" %}{{ group }}{% endfor %}
        """)
        numbers = range(9)
        c = template.Context({
            'objects': numbers,
        })
        o = t.render(c).strip()
       
        self.assertEquals(o, unicode(numbers[0:5]) + unicode(numbers[5:]))

    def test_split_list_4(self):
        t = template.Template("""
        {% load list_tags %}
        {% for group in objects|split_list:"-1" %}{{ group }}{% endfor %}
        """)
        numbers = range(14)
        c = template.Context({
            'objects': numbers,
        })
        o = t.render(c).strip()
       
        self.assertEquals(o, '')

    def test_split_list_4(self):
        t = template.Template("""
        {% load list_tags %}
        {% for group in objects|split_list:"0" %}{{ group }}{% endfor %}
        """)
        numbers = range(5)
        c = template.Context({
            'objects': numbers,
        })
        o = t.render(c).strip()
       
        self.assertEquals(o, '')

class StringTagsTest(test.TestCase):
    def test_ensure_sentence_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load string_tags %}
            {{ "FooBar"|ensure_sentence:"" }}
            """)

        self.assertEquals('ensure_sentence requires 0 arguments, 1 provided', str(cm.exception))

    def _test_string(self, first, second):
        t = template.Template("""
        {% load string_tags %}
        {{ string|ensure_sentence }}
        """)

        c = template.Context({
            'string': first,
        })
        o = t.render(c).strip()
        self.assertEquals(o, second)

    def test_ensure_sentence_2(self):
        self._test_string('FooBar', 'FooBar.')
    
    def test_ensure_sentence_3(self):
        self._test_string('FooBar.', 'FooBar.')

    def test_ensure_sentence_3(self):
        self._test_string('FooBar?', 'FooBar?')

class UrlTagsTest(test.TestCase):
    def setUp(self):
        self.factory = client.RequestFactory()

    def test_slugify2_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load url_tags %}
            {{ "FooBar"|slugify2:"" }}
            """)

        self.assertEquals('slugify2 requires 0 arguments, 1 provided', str(cm.exception))

    def _test_string(self, first, second):
        t = template.Template("""
        {% load url_tags %}
        {{ string|slugify2 }}
        """)

        c = template.Context({
            'string': first,
        })
        o = t.render(c).strip()
        self.assertEquals(o, second)

    def test_slugify2_2(self):
        self._test_string(u'Işık ılık süt iç', u'isik-ilik-sut-ic')

    def test_slugify2_2(self):
        self._test_string(u'ČĆŽŠĐ čćžšđ', u'cczsdj-cczsdj')

    def _test_url(self, url):
        request = self.factory.get('/foo/')

        t = template.Template("""
        {% load url_tags %}
        {% fullurl url %}
        """)

        c = template.RequestContext(request, {
            'request': request,
            'url': url,
        })
        o = t.render(c).strip()
        self.assertEquals(o, request.build_absolute_uri(url))

    def test_fullurl_1(self):
        request = self.factory.get('/foo/')

        t = template.Template("""
        {% load url_tags %}
        {% fullurl %}
        """)

        c = template.RequestContext(request, {
            'request': request,
        })
        o = t.render(c).strip()
        self.assertEquals(o, request.build_absolute_uri())

    def test_fullurl_2(self):
        self._test_url(None)

    def test_fullurl_3(self):
        self._test_url('/bar/')
