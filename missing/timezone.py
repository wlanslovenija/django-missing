import datetime

from django.utils import timezone

def to_date(value):
    """
    Function which knows how to convert timezone-aware :py:class:`~datetime.datetime` objects to
    :py:class:`~datetime.date` objects, according to guidelines from `Django documentation`_.

    .. _Django documentation: https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#troubleshooting
    """

    assert isinstance(value, (datetime.date, datetime.datetime))

    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value

    if timezone.is_aware(value) and timezone.pytz:
        current_timezone = timezone.get_current_timezone()
        return current_timezone.normalize(value.astimezone(current_timezone)).date()
    else:
        return value.date()
