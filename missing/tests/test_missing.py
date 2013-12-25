# -*- coding: utf-8 -*-

from __future__ import with_statement

import django
from django import template, test as django_test
from django.core import urlresolvers
from django.test import client
from django.utils import html, unittest
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

    def test_split_list_5(self):
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

    def test_ensure_sentence_4(self):
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

    def test_slugify2_3(self):
        self._test_string(u'ČĆŽŠĐ čćžšđ', u'cczsdj-cczsdj')

    def test_slugify2_4(self):
        self._test_string(u'..test foobar..', u'test-foobar')

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

@unittest.skipUnless(django.VERSION >= (1, 4), "Tag supported only for Django >= 1.4")
class UrlTemplateTest(django_test.TestCase):
    urls = 'missing.tests.urltemplate_urls'

    def setUp(self):
        self.factory = client.RequestFactory()

    def _test_urltemplate(self, params, result):
        with self.settings(TEMPLATE_DEBUG=True):
            t = template.Template("""
            {%% load url_tags %%}
            {%% urltemplate %s %%}
            """ % params)

            c = template.Context()
            o = t.render(c).strip()
            self.assertEquals(o, result)

    def test_urltemplate_simply(self):
        self._test_urltemplate('"test1"', '/test1/')

    def test_urltemplate_nonexistent(self):
        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"nonexistent"', '')

    def test_urltemplate_mix(self):
        with self.assertRaisesMessage(ValueError, "Don't mix *args and **kwargs."):
            self._test_urltemplate('"test_kwargs" "2000" month="12"', '/test_kwargs/2000/12/{day}/')

    def test_urltemplate_args1(self):
        self._test_urltemplate('"test_args"', '/test_args/{0}/{1}/{2}/')

    def test_urltemplate_args2(self):
        self._test_urltemplate('"test_args" "2000"', '/test_args/2000/{1}/{2}/')
        self._test_urltemplate('"test_args" "2000" "12"', '/test_args/2000/12/{2}/')
        self._test_urltemplate('"test_args" "2000" "12" "1"', '/test_args/2000/12/1/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_args" year="2000"', '/test_args/2000/{month}/{day}/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_args" "2000" "12" "1" "foobar"', '/test_args/2000/12/1/')

    def test_urltemplate_kwargs1(self):
        self._test_urltemplate('"test_kwargs"', '/test_kwargs/{year}/{month}/{day}/')

    def test_urltemplate_kwargs2(self):
        self._test_urltemplate('"test_kwargs" "2000"', '/test_kwargs/2000/{month}/{day}/')
        self._test_urltemplate('"test_kwargs" "2000" "12"', '/test_kwargs/2000/12/{day}/')
        self._test_urltemplate('"test_kwargs" "2000" "12" "1"', '/test_kwargs/2000/12/1/')

        self._test_urltemplate('"test_kwargs" year="2000"', '/test_kwargs/2000/{month}/{day}/')
        self._test_urltemplate('"test_kwargs" year="2000" month="12"', '/test_kwargs/2000/12/{day}/')
        self._test_urltemplate('"test_kwargs" year="2000" month="12" day="1"', '/test_kwargs/2000/12/1/')
        self._test_urltemplate('"test_kwargs" year="2000" day="1"', '/test_kwargs/2000/{month}/1/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_kwargs" "2000" "12" "1" "foobar"', '/test_kwargs/2000/12/1/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_kwargs" foobar="42"', '/test_kwargs/{year}/{month}/{day}/')

    def test_urltemplate_mixed1(self):
        self._test_urltemplate('"test_mixed"', '/test_mixed/{year}/{0}/{day}/')

    def test_urltemplate_mixed2(self):
        self._test_urltemplate('"test_mixed" "2000"', '/test_mixed/2000/{0}/{day}/')
        self._test_urltemplate('"test_mixed" "2000" "12"', '/test_mixed/2000/12/{day}/')
        self._test_urltemplate('"test_mixed" "2000" "12" "1"', '/test_mixed/2000/12/1/')

        self._test_urltemplate('"test_mixed" year="2000"', '/test_mixed/2000/{0}/{day}/')
        self._test_urltemplate('"test_mixed" year="2000" day="1"', '/test_mixed/2000/{0}/1/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_mixed" "2000" "12" "1" "foobar"', '/test_mixed/2000/12/1/')

        with self.assertRaises(urlresolvers.NoReverseMatch):
            self._test_urltemplate('"test_mixed" foobar="42"', '/test_mixed/{year}/{month}/{day}/')

    def test_urltemplate_possible1(self):
        self._test_urltemplate('"test_possible"', '/test_possible/{month}/{day}/')

    def test_urltemplate_possible2(self):
        self._test_urltemplate('"test_possible" month="12"', '/test_possible/12/{day}/')

    def test_urltemplate_possible3(self):
        self._test_urltemplate('"test_possible" year="2000"', '/test_possible/2000/{day}/')

    def test_urltemplate_api(self):
        self._test_urltemplate('"api_get_schema"', '/api/{api_name}/{resource_name}/schema/')
        self._test_urltemplate('"api_get_schema" api_name="v1"', '/api/v1/{resource_name}/schema/')

    def test_urltemplate_example(self):
        with self.settings(TEMPLATE_DEBUG=True):
            t = template.Template("""
            {% load url_tags %}
            {% with variable="42" %}
                {% urltemplate "view_name" arg1="value" arg2=variable %}
            {% endwith %}
            """)

            c = template.Context()
            o = t.render(c).strip()
            self.assertEquals(o, '/some/view/value/42/{param}/')

@unittest.skipUnless(django.VERSION >= (1, 4), "Only Django >= 1.4 has DEFAULT_EXCEPTION_REPORTER_FILTER")
class SafeExceptionReporterFilterTest(django_test.TestCase):
    urls = 'missing.tests.safereporting_urls'

    def setUp(self):
        self.c = test.Client(TEST_PASSWORD='foobar', TEST_COOKIE='foobar')

    def test_failure(self):
        with self.settings(DEBUG=True, DEFAULT_EXCEPTION_REPORTER_FILTER='missing.debug.SafeExceptionReporterFilter'):
            response = self.c.get('/failure/')

            self.assertEqual(response.context['settings']['ROOT_URLCONF'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['settings']['CSRF_COOKIE_DOMAIN'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['TEST_PASSWORD'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['HTTP_COOKIE'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['TEST_COOKIE'], debug.CLEANSED_SUBSTITUTE)

class HTMLTagsTest(django_test.TestCase):
    def test_heading_1(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h1 id="test" class="heading ">Test</h1>""")

    def test_heading_2(self):
        t = template.Template("""
        {% load html_tags %}
        {% set_base_heading_level 3 %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h4 id="test" class="heading ">Test</h4>""")

    def test_heading_3(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" "test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h1 id="test" class="heading test">Test</h1>""")

    def test_heading_4(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Longer test with spaces and various characters!?" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h1 id="longer-test-with-spaces-and-various-characters" class="heading ">Longer test with spaces and various characters!?</h1>""")

    def test_heading_5(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "12345" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h1 id="a12345" class="heading ">12345</h1>""")

    def test_heading_6(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = html.strip_spaces_between_tags(t.render(c).strip())
        self.assertEquals(o, """<h1 id="test" class="heading ">Test</h1><h1 id="test-0" class="heading ">Test</h1>""")

    def test_heading_7(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h4 id="test" class="heading ">Test</h4>""")

    def test_heading_8(self):
        t = template.Template("""
        {% load html_tags %}
        {% set_base_heading_level 2 %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h3 id="test" class="heading ">Test</h3>""")

    def test_heading_9(self):
        t = template.Template("""
        {% load html_tags %}
        {% with base_heading_level=2 %}
            {% heading 1 "Test" %}
        {% endwith %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h3 id="test" class="heading ">Test</h3>""")

    def test_heading_10(self):
        t = template.Template("""
        {% load html_tags %}
        {% with base_heading_level=2 %}
        {% endwith %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h4 id="test" class="heading ">Test</h4>""")

    def test_heading_11(self):
        t = template.Template("""
        {% load html_tags %}
        {% with base_heading_level=2 %}
            {% set_base_heading_level 4 %}
        {% endwith %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h4 id="test" class="heading ">Test</h4>""")

    def test_heading_12(self):
        t = template.Template("""
        {% load html_tags %}
        {% with base_heading_level=2 %}
            {% set_base_heading_level 4 "True" %}
        {% endwith %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEquals(o, """<h5 id="test" class="heading ">Test</h5>""")

    def test_anchorify_example(self):
        t = template.Template("""
        {% load i18n html_tags %}
        <h1 id="{{ _("My Blog")|anchorify }}">{% trans "My Blog" %}</h1>
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEquals(o, """<h1 id="my-blog">My Blog</h1>""")
