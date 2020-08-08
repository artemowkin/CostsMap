"""Module with dates utilities"""

import datetime
from monthdelta import monthdelta


class BaseContextDate:

    """Abstract class for dates in template context

    Properties
    ----------
    date : str
        Return string with current date

    """

    def __init__(self, date: datetime.date = None):
        if not date:
            date = datetime.date.today()

        self._date = date

    @property
    def date(self):
        """Return ISO string with current date"""
        return self._date.isoformat()


class ContextDate(BaseContextDate):

    """ContextDate with previous_day and next_day properties

    Properties
    ----------
    previous_day : str
        Return string with previous day date

    next_day : str
        Return string with next day date

    """

    @property
    def previous_day(self):
        """Return ISO string of previous day date"""
        prev_date = self._date - datetime.timedelta(days=1)
        return prev_date.isoformat()

    @property
    def next_day(self):
        """Return ISO string of next day date"""
        next_date = self._date + datetime.timedelta(days=1)
        return next_date.isoformat()


class MonthContextDate(BaseContextDate):

    """ContextDate with previous_month and next_month properties

    Properties
    ----------
    date : str
        Return string with current date without days

    previous_month : str
        Return string with previous month date

    next_month : str
        Return string with next_month date

    """

    @property
    def date(self):
        """Return date in format <year>-<month>"""
        return super().date[:-3]

    @property
    def previous_month(self):
        """Return previous month in format <year>-<month>"""
        previous_month = self._date - monthdelta(1)
        return previous_month.isoformat()[:-3]

    @property
    def next_month(self):
        """Return next month in format <year>-<month>"""
        next_month = self._date + monthdelta(1)
        return next_month.isoformat()[:-3]

