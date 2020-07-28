"""Module with templates tools"""

import datetime


class ContextDate:

    """
    Date with previous_day and next_day properties for template context
    """

    def __init__(self, date: str):
        self._date = date
        self._date_obj = datetime.date.fromisoformat(date)

    @property
    def date(self):
        """Return current date"""
        return self._date

    @property
    def previous_day(self):
        """Return ISO string of previous day date"""
        prev_date_obj = self._date_obj - datetime.timedelta(days=1)
        return prev_date_obj.isoformat()

    @property
    def next_day(self):
        """Return ISO string of next day date"""
        next_date_obj = self._date_obj + datetime.timedelta(days=1)
        return next_date_obj.isoformat()

