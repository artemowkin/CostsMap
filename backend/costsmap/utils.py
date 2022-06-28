from decimal import Decimal


def validate_amount_max_min(amount: Decimal):
    """Validate is amount less than max value and more than min value"""
    if amount < Decimal('0.01') or amount > Decimal('9999999.99'):
        raise ValueError("Amount must be more than 0 and less than 10000000")
