"""CLI interface."""

import sys

from src.validator import validate_pan_masking, MaskingError


def main():
    if len(sys.argv) < 2:
        print("Usage: pan-validate <pan>")
        print("Validate PAN masking according to PCI DSS 3.3")
        print("Example: pan-validate '123456******1234'")
        return 1

    pan = sys.argv[1]

    try:
        validate_pan_masking(pan)
        print("Valid: PAN is properly masked")
        return 0
    except MaskingError as e:
        print(f"Invalid: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
