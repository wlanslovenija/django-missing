# -*- coding: utf-8 -*-

from __future__ import with_statement

from django import template, test as django_test

from missing.templatetags.string_tags import endswith

try:
    from django import urls
except ImportError:
    from django.core import urlresolvers as urls
from django.test import client
from django.utils import html
# Remove this check when support for Python 2 is dropped.
# https://docs.djangoproject.com/en/3.0/releases/3.0/#django-utils-encoding-force-text-and-smart-text
import sys
if sys.version_info[0] >= 3:
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str
from django.views import debug


class NoErrorClient(client.Client):
    """
    Test client which does not specially handle exceptions.

    Useful for testing HTTP 500 error handlers.
    """

    def store_exc_info(self, **kwargs):
        pass


@django_test.override_settings(ROOT_URLCONF='missing.tests.context_urls')
class ContextTagsTest(django_test.TestCase):
    def test_setcontext_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% setcontext foo bar %}
            FooBar
            {% endsetcontext %}
            """)

        self.assertIn('tag takes 2 arguments and the first argument', str(cm.exception))

    def test_setcontext_2(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% setcontext %}
            FooBar
            {% endsetcontext %}
            """)

        self.assertIn('tag takes 2 arguments and the first argument', str(cm.exception))

    def test_setcontext_3(self):
        t = template.Template("""
        {% setcontext as variable %}
        FooBar
        {% endsetcontext %}
        """)
        c = template.Context()
        o = t.render(c).strip()

        self.assertIn('variable', c)
        self.assertEqual(c['variable'].strip(), 'FooBar')
        self.assertEqual(o, '')

    def test_contextblock_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {{ something }}
            {% contextblock %}
            {% endcontextblock %}
            """)

        self.assertIn('must be the first tag in the template', str(cm.exception))

    def test_contextblock_2(self):
        base = template.Template("""
        {% contextblock %}{% if double_call %}{% setcontext as bug %}bug{% endsetcontext %}{% endif %}{% endcontextblock %}{% spaceless %}<html>
            <body>
                <head>
                    <title>{{ title }}</title>
                </head>
                <body>
                    <h1>{{ title }}</h1>
                    <p><a href="{{ homepage }}">{{ title }}</a></p>
                </body>
            </body>
        </html>{% endspaceless %}""")

        t = template.Template("""
        {% extends base %}

        {% contextblock %}
            {% load i18n %}
            {% setcontext as title %}{% blocktrans %}{{ username }}'s blog{% endblocktrans %}{% endsetcontext %}
            {% url "homepage" as homepage %}
            {% setcontext as double_call %}true{% endsetcontext %}
            {{ block.super }}
        {% endcontextblock %}
        """)

        c = template.Context({
            'username': 'Username',
            'base': base,
        })
        o = t.render(c).strip()

        self.assertNotIn('bug', c)
        self.assertEqual(o, """<html><body><head><title>Username's blog</title></head><body><h1>Username's blog</h1><p><a href="/homepage/">Username's blog</a></p></body></body></html>""")

    def test_contextblock_3(self):
        base = template.Template("""
            {% contextblock %}{% if double_call %}{% setcontext as bug %}bug{% endsetcontext %}{% endif %}{% setcontext as double_call %}true{% endsetcontext %}{% endcontextblock %}{% spaceless %}<html>
            <body>
                <head>
                    <title>{{ title }}</title>
                </head>
                <body>
                    <h1>{{ title }}</h1>
                    <p><a href="{{ homepage }}">{{ title }}</a></p>
                </body>
            </body>
        </html>{% endspaceless %}""")

        t = template.Template("""
        {% extends base %}

        {% contextblock %}
            {% load i18n %}
            {% setcontext as title %}{% blocktrans %}{{ username }}'s blog{% endblocktrans %}{% endsetcontext %}
            {% url "homepage" as homepage %}
            {{ block.super }}
        {% endcontextblock %}
        """)

        c = template.Context({
            'username': 'Username',
            'base': base,
        })
        o = t.render(c).strip()

        self.assertNotIn('bug', c)
        self.assertEqual(o, """<html><body><head><title>Username's blog</title></head><body><h1>Username's blog</h1><p><a href="/homepage/">Username's blog</a></p></body></body></html>""")


    def test_contextblock_4(self):
        base1 = template.Template("""
        {% contextblock %}{% if double_call %}{% setcontext as bug %}bug{% endsetcontext %}{% endif %}{% endcontextblock %}{% spaceless %}<html>
            <body>
                <head>
                    <title>{{ title }}</title>
                </head>
                <body>
                    <h1>{{ title }}</h1>
                    <p><a href="{{ homepage }}">{{ title }}</a></p>
                </body>
            </body>
        </html>{% endspaceless %}""")

        base2 = template.Template("""
        {% extends base1 %}

        {% contextblock %}
            {% url "homepage" as homepage %}
        {% endcontextblock %}
        """)

        t = template.Template("""
        {% extends base2 %}

        {% contextblock %}
            {% load i18n %}
            {% setcontext as title %}{% blocktrans %}{{ username }}'s blog{% endblocktrans %}{% endsetcontext %}
            {% setcontext as double_call %}true{% endsetcontext %}
            {{ block.super }}
        {% endcontextblock %}
        """)

        c = template.Context({
            'username': 'Username',
            'base1': base1,
            'base2': base2,
        })
        o = t.render(c).strip()

        self.assertNotIn('bug', c)
        self.assertEqual(o, """<html><body><head><title>Username's blog</title></head><body><h1>Username's blog</h1><p><a href="/homepage/">Username's blog</a></p></body></body></html>""")

    def test_contextblock_5(self):
        base1 = template.Template("""
        {% contextblock %}{% endcontextblock %}{% spaceless %}<html>
            <body>
                <head>
                    <title>{{ title }}</title>
                </head>
                <body>
                    <h1>{{ title }}</h1>
                    <p><a href="{{ homepage }}">{{ title }}</a></p>
                </body>
            </body>
        </html>{% endspaceless %}""")

        base2 = template.Template("""
        {% extends base1 %}

        {% contextblock %}
            {% url "homepage" as homepage %}

            {% if double_call %}{% setcontext as bug %}bug{% endsetcontext %}{% endif %}
            {% setcontext as double_call %}true{% endsetcontext %}
        {% endcontextblock %}""")

        t = template.Template("""
        {% extends base2 %}

        {% contextblock %}
            {% load i18n %}
            {% setcontext as title %}{% blocktrans %}{{ username }}'s blog{% endblocktrans %}{% endsetcontext %}
            {{ block.super }}
        {% endcontextblock %}
        """)

        c = template.Context({
            'username': 'Username',
            'base1': base1,
            'base2': base2,
        })
        o = t.render(c).strip()

        self.assertNotIn('bug', c)
        self.assertEqual(o, """<html><body><head><title>Username's blog</title></head><body><h1>Username's blog</h1><p><a href="/homepage/">Username's blog</a></p></body></body></html>""")


class LangTagsTest(django_test.TestCase):
    def test_translate_2(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load lang_tags %}
            {% translate "FooBar" %}
            """)

        self.assertEqual("'translate' did not receive value(s) for the argument(s): 'lang_code'", str(cm.exception))


class ListTagsTest(django_test.TestCase):
    def test_split_list_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load list_tags %}
            {{ objects|split_list }}
            """)

        self.assertEqual('split_list requires 2 arguments, 1 provided', str(cm.exception))

    def test_split_list_2(self):
        t = template.Template("""
        {% load list_tags %}
        |{% for group in objects|split_list:"4" %}{{ group|length }}|{% endfor %}
        """)
        c = template.Context({
            'objects': range(10),
        })
        o = t.render(c).strip()

        self.assertEqual(o, '|4|4|2|')

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

        self.assertEqual(o, force_str(list(numbers[0:5])) + force_str(list(numbers[5:])))

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

        self.assertEqual(o, '')

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

        self.assertEqual(o, '')


class StringTagsTest(django_test.TestCase):
    def test_ensure_sentence_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load string_tags %}
            {{ "FooBar"|ensure_sentence:"" }}
            """)

        self.assertEqual('ensure_sentence requires 1 arguments, 2 provided', str(cm.exception))

    def _test_string(self, first, second):
        t = template.Template("""
        {% load string_tags %}
        {{ string|ensure_sentence }}
        """)

        c = template.Context({
            'string': first,
        })
        o = t.render(c).strip()
        self.assertEqual(o, second)

    def test_ensure_sentence_2(self):
        self._test_string('FooBar', 'FooBar.')

    def test_ensure_sentence_3(self):
        self._test_string('FooBar.', 'FooBar.')

    def test_ensure_sentence_4(self):
        self._test_string('FooBar?', 'FooBar?')

    def test_endswith(self):
        self.assertTrue(endswith("foobar", "bar"))
        self.assertFalse(endswith("foobar", "foo"))


class UrlTagsTest(django_test.TestCase):
    def setUp(self):
        self.factory = client.RequestFactory()

    def test_slugify2_1(self):
        with self.assertRaises(template.TemplateSyntaxError) as cm:
            t = template.Template("""
            {% load url_tags %}
            {{ "FooBar"|slugify2:"" }}
            """)

        self.assertEqual('slugify2 requires 1 arguments, 2 provided', str(cm.exception))

    def _test_string(self, first, second):
        t = template.Template("""
        {% load url_tags %}
        {{ string|slugify2 }}
        """)

        c = template.Context({
            'string': first,
        })
        o = t.render(c).strip()
        self.assertEqual(o, second)

    def test_slugify2_2(self):
        with self.settings(DEBUG=True):
            self._test_string(u'Işık ılık süt iç', u'isik-ilik-sut-ic')

    def test_slugify2_3(self):
        with self.settings(DEBUG=True):
            self._test_string(u'ČĆŽŠĐ čćžšđ', u'cczsdj-cczsdj')

    def test_slugify2_4(self):
        with self.settings(DEBUG=True):
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
        self.assertEqual(o, request.build_absolute_uri(url))

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
        self.assertEqual(o, request.build_absolute_uri())

    def test_fullurl_2(self):
        self._test_url(None)

    def test_fullurl_3(self):
        self._test_url('/bar/')


@django_test.override_settings(ROOT_URLCONF='missing.tests.urltemplate_urls')
class UrlTemplateTest(django_test.TestCase):
    def setUp(self):
        self.factory = client.RequestFactory()

    def _test_urltemplate(self, params, result):
        with self.settings(DEBUG=True):
            t = template.Template("""
            {%% load url_tags %%}
            {%% urltemplate %s %%}
            """ % params)

            c = template.Context()
            o = t.render(c).strip()
            self.assertEqual(o, result)

    def test_urltemplate_simply(self):
        self._test_urltemplate('"test1"', '/test1/')

    def test_urltemplate_nonexistent(self):
        with self.assertRaises(urls.NoReverseMatch):
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

        with self.assertRaises(urls.NoReverseMatch):
            self._test_urltemplate('"test_args" year="2000"', '/test_args/2000/{month}/{day}/')

        with self.assertRaises(urls.NoReverseMatch):
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

        with self.assertRaises(urls.NoReverseMatch):
            self._test_urltemplate('"test_kwargs" "2000" "12" "1" "foobar"', '/test_kwargs/2000/12/1/')

        with self.assertRaises(urls.NoReverseMatch):
            self._test_urltemplate('"test_kwargs" foobar="42"', '/test_kwargs/{year}/{month}/{day}/')

    def test_urltemplate_mixed1(self):
        self._test_urltemplate('"test_mixed"', '/test_mixed/{year}/{0}/{day}/')

    def test_urltemplate_mixed2(self):
        self._test_urltemplate('"test_mixed" "2000"', '/test_mixed/2000/{0}/{day}/')
        self._test_urltemplate('"test_mixed" "2000" "12"', '/test_mixed/2000/12/{day}/')
        self._test_urltemplate('"test_mixed" "2000" "12" "1"', '/test_mixed/2000/12/1/')

        self._test_urltemplate('"test_mixed" year="2000"', '/test_mixed/2000/{0}/{day}/')
        self._test_urltemplate('"test_mixed" year="2000" day="1"', '/test_mixed/2000/{0}/1/')

        with self.assertRaises(urls.NoReverseMatch):
            self._test_urltemplate('"test_mixed" "2000" "12" "1" "foobar"', '/test_mixed/2000/12/1/')

        with self.assertRaises(urls.NoReverseMatch):
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
        with self.settings(DEBUG=True):
            t = template.Template("""
            {% load url_tags %}
            {% with variable="42" %}
                {% urltemplate "view_name" arg1="value" arg2=variable %}
            {% endwith %}
            """)

            c = template.Context()
            o = t.render(c).strip()
            self.assertEqual(o, '/some/view/value/42/{param}/')


@django_test.override_settings(ROOT_URLCONF='missing.tests.safereporting_urls')
class SafeExceptionReporterFilterTest(django_test.TestCase):
    def setUp(self):
        self.c = NoErrorClient(TEST_PASSWORD='foobar', TEST_COOKIE='foobar', TEST_NORMAL='ok')

    def test_failure(self):
        with self.settings(DEBUG=True, DEFAULT_EXCEPTION_REPORTER_FILTER='missing.debug.SafeExceptionReporterFilter'):
            response = self.c.get('/failure/')

            self.assertEqual(response.context['settings']['ROOT_URLCONF'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['settings']['CSRF_COOKIE_DOMAIN'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['TEST_PASSWORD'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['HTTP_COOKIE'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['TEST_COOKIE'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(response.context['request'].META['TEST_NORMAL'], 'ok')

            response = self.c.post('/failure/', data={'csrfmiddlewaretoken': 'abcde', 'normal': 'ok'})
            # In Django >= 1.11.
            if 'filtered_POST_items' in response.context:
                post_items = dict(response.context['filtered_POST_items'])
            else:
                post_items = response.context['filtered_POST']
            self.assertEqual(post_items['csrfmiddlewaretoken'], debug.CLEANSED_SUBSTITUTE)
            self.assertEqual(post_items['normal'], 'ok')


@django_test.override_settings(DEBUG=True)
class HTMLTagsTest(django_test.TestCase):
    def test_heading_1(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h1 id="test" class="heading ">Test</h1>""")

    def test_heading_2(self):
        t = template.Template("""
        {% load html_tags %}
        {% set_base_heading_level 3 %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h4 id="test" class="heading ">Test</h4>""")

    def test_heading_3(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" "test" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h1 id="test" class="heading test">Test</h1>""")

    def test_heading_4(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Longer test with spaces and various characters!?" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h1 id="longer-test-with-spaces-and-various-characters" class="heading ">Longer test with spaces and various characters!?</h1>""")

    def test_heading_5(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "12345" %}
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h1 id="a12345" class="heading ">12345</h1>""")

    def test_heading_6(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        {% heading 1 "Test" %}
        """)

        c = template.Context()
        o = html.strip_spaces_between_tags(t.render(c).strip())
        self.assertEqual(o, """<h1 id="test" class="heading ">Test</h1><h1 id="test-0" class="heading ">Test</h1>""")

    def test_heading_7(self):
        t = template.Template("""
        {% load html_tags %}
        {% heading 1 "Test" %}
        """)

        c = template.Context({
            'base_heading_level': 3,
        })
        o = t.render(c).strip()
        self.assertEqual(o, """<h4 id="test" class="heading ">Test</h4>""")

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
        self.assertEqual(o, """<h3 id="test" class="heading ">Test</h3>""")

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
        self.assertEqual(o, """<h3 id="test" class="heading ">Test</h3>""")

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
        self.assertEqual(o, """<h4 id="test" class="heading ">Test</h4>""")

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
        self.assertEqual(o, """<h4 id="test" class="heading ">Test</h4>""")

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
        self.assertEqual(o, """<h5 id="test" class="heading ">Test</h5>""")

    def test_anchorify_example(self):
        t = template.Template("""
        {% load i18n html_tags %}
        <h1 id="{{ _("My Blog")|anchorify }}">{% trans "My Blog" %}</h1>
        """)

        c = template.Context()
        o = t.render(c).strip()
        self.assertEqual(o, """<h1 id="my-blog">My Blog</h1>""")
