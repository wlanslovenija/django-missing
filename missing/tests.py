# -*- coding: utf-8 -*-

from __future__ import with_statement

import django
from django import template
from django import test as django_test
from django.test import client, utils
from django.utils import unittest
from django.views import debug

from missing import test

class ContextTagsTest(django_test.TestCase):
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

class LangTagsTest(django_test.TestCase):
    @unittest.skipUnless(django.VERSION < (1, 4), "Test for Django < 1.4")
    def test_translate_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load lang_tags %}
            {% translate "FooBar" %}
            """)

        self.assertEquals('translate takes 2 arguments', str(cm.exception))

    @unittest.skipUnless(django.VERSION >= (1, 4), "Test for Django >= 1.4")
    def test_translate_2(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load lang_tags %}
            {% translate "FooBar" %}
            """)

        self.assertEquals("'translate' did not receive value(s) for the argument(s): 'lang_code'", str(cm.exception))

class ListTagsTest(django_test.TestCase):
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

class StringTagsTest(django_test.TestCase):
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

class UrlTagsTest(django_test.TestCase):
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

@utils.override_settings(DEBUG=True)
class SafeExceptionReporterFilterTest(django_test.TestCase):
    def setUp(self):
        self.c = test.Client(TEST_PASSWORD='foobar', TEST_COOKIE='foobar')

    @unittest.skipUnless(django.VERSION >= (1, 4), "Test for Django >= 1.4")
    def test_failure(self):
        response = self.c.get('/failure/')

        self.assertEqual(response.context['settings']['ROOT_URLCONF'], debug.CLEANSED_SUBSTITUTE)
        self.assertEqual(response.context['settings']['CSRF_COOKIE_DOMAIN'], debug.CLEANSED_SUBSTITUTE)
        self.assertEqual(response.context['request'].META['TEST_PASSWORD'], debug.CLEANSED_SUBSTITUTE)
        self.assertEqual(response.context['request'].META['HTTP_COOKIE'], debug.CLEANSED_SUBSTITUTE)
        self.assertEqual(response.context['request'].META['TEST_COOKIE'], debug.CLEANSED_SUBSTITUTE)
