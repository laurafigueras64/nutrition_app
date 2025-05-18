def get_number_or_zero(value):
    """Convert input to float or return 0.0 if empty or invalid."""
    value = str(value).strip()
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
