from decimal import Decimal, ROUND_DOWN

def quantize_amount(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
