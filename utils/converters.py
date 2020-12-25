import datetime


class ISODateConverter:
    """Converter to check is date in ISO format"""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value: str) -> datetime.date:
        return datetime.date.fromisoformat(value)

    def to_url(self, value: datetime.date) -> str:
        if isinstance(value, datetime.date):
            return value.isoformat()

        return value


class MonthYearConverter:
    """Converter to check is date in `<year>-<month>` format"""

    regex = r'\d{4}-\d{2}'

    def to_python(self, value: str) -> datetime.date:
        value = value + '-01'
        return datetime.date.fromisoformat(value)

    def to_url(self, value: datetime.date) -> str:
        if isinstance(value, datetime.date):
            return value.isoformat()[:-3]

        return value


class YearConverter:
    """Converter to check is date in `yyyy` format"""

    regex = r'\d{4}'

    def to_python(self, value: str) -> datetime.date:
        value = value + '-01-01'
        return datetime.date.fromisoformat(value)

    def to_url(self, value: datetime.date) -> str:
        if isinstance(value, datetime.date):
            return value.isoformat()[:4]

        return value
