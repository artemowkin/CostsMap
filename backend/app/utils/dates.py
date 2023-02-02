import datetime

from dateutil.relativedelta import relativedelta


def get_current_month() -> str:
    """Returns current month in format YYYY-MM"""
    return str(datetime.date.today())[:-3]


def get_month_delta(month: str) -> tuple[datetime.date, datetime.date]:
    """Returns date delta (month start date and month end date)
    
    :param month: Month in format YYYY-MM
    """
    start_date = datetime.date.fromisoformat(month + '-01')
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
    return start_date, end_date
