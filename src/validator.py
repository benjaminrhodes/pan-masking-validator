"""PAN masking validator."""

import re


class MaskingError(Exception):
    """Exception raised for PAN masking validation errors."""

    pass


def validate_pan_masking(pan: str) -> bool:
    """Validate that a PAN is properly masked according to PCI DSS 3.3.

    Args:
        pan: The PAN string to validate.

    Returns:
        True if the PAN is properly masked.

    Raises:
        MaskingError: If the PAN is not properly masked.
    """
    if not pan:
        raise MaskingError("PAN cannot be empty")

    for char in pan:
        if char.isdigit():
            continue
        if char == "*":
            continue
        if char in " -":
            continue
        raise MaskingError("Mask must use asterisk (*) character")

    visible_digits = re.sub(r"[^0-9]", "", pan)
    cleaned = re.sub(r"[^0-9*]", "", pan)

    if len(visible_digits) == 0:
        raise MaskingError("PAN is not masked")

    if len(visible_digits) > 10:
        raise MaskingError("Too many visible digits: must show at most first 6 and last 4")

    if len(visible_digits) < 10:
        raise MaskingError("Must show first 6 and last 4 digits")

    if cleaned[:6].count("*") > 0:
        raise MaskingError("First 6 digits must be visible")

    if cleaned[-4:].count("*") > 0:
        raise MaskingError("Last 4 digits must be visible")

    return True
