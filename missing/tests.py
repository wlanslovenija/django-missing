from django import template
from django import test

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
