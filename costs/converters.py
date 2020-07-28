class ISODateConverter:

    """Converter to check is date in ISO format"""

    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return str(value)

