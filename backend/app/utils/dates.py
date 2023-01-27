from datetime import date


def get_current_month() -> str:
    """Returns current month in format YYYY-MM"""
    return str(date.today())[:-3]