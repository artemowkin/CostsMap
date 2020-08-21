"""Module with urlpattern's converters"""

import datetime


class ISODateConverter:

    """Converter to check is date in ISO format"""

    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        if isinstance(value, datetime.date):
            return value.isoformat()

        return value


class MonthYearConverter:

    """Converter to check is date in `<year>-<month>` format"""

    regex = '\d{4}-\d{2}'

    def to_python(self, value):
        value = value + '-01'
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        if isinstance(value, datetime.date):
            return value.isoformat()[:-3]

        return value


class YearConverter:

    """Converter to check is date in `yyyy` format"""

    regex = '\d{4}'

    def to_python(self, value):
        value = value + '-01-01'
        return datetime.date.fromisoformat(value)

    def to_url(self, value):
        if isinstance(value, datetime.date):
            return value.isoformat()[:4]

        return value

