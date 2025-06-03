
"""billing package – public façade over billing.calculator"""
from importlib import metadata as _metadata
from .calculator import (
    price_with_tax,
    apply_coupon,
    compute_total,
    compute_subtotal,
    booking_fee,
    convert_currency,
    loyalty_points_earned,
    compute_bulk_total,
    _round,
    validate_coupon,
    split_payment,
    SUPPORTED_CURRENCIES,
    parse_iso_date,
    compute_refund,
    bulk_discount,
    tax_breakdown,
    TAX_RATE,
    validate_tax_number,
    apply_dynamic_tax,
    LOYALTY_POINT_RATE,
    apply_loyalty_discount,
    cap_price,
    round_money,
    is_weekend_rate
)

__all__ = [
    "price_with_tax", "apply_coupon", "compute_total", "compute_subtotal",
    "booking_fee", "convert_currency", "loyalty_points_earned",
    "compute_bulk_total",
]

try:
    __version__ = _metadata.version(__name__)
except _metadata.PackageNotFoundError:
    __version__ = "0.1.0"
