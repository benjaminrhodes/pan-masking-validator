"""Tests for PAN masking validator."""

import pytest

from src.validator import validate_pan_masking, MaskingError


class TestValidatePanMasking:
    """Tests for validate_pan_masking function."""

    def test_valid_masked_pan_simple_format(self):
        """Test valid masked PAN in simple format."""
        result = validate_pan_masking("123456******1234")
        assert result is True

    def test_valid_masked_pan_with_dashes(self):
        """Test valid masked PAN with dashes."""
        result = validate_pan_masking("1234-56**-****-1234")
        assert result is True

    def test_valid_masked_pan_with_spaces(self):
        """Test valid masked PAN with spaces."""
        result = validate_pan_masking("1234 56** **** 1234")
        assert result is True

    def test_valid_masked_pan_16_digits(self):
        """Test valid masked PAN with 16 digits."""
        result = validate_pan_masking("123456******1234")
        assert result is True

    def test_valid_masked_pan_15_digits(self):
        """Test valid masked PAN with 15 digits (Amex)."""
        result = validate_pan_masking("123456*******1234")
        assert result is True

    def test_unmasked_pan_raises_error(self):
        """Test unmasked full PAN raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("1234567890123456")
        assert "too many" in str(exc_info.value).lower() or "mask" in str(exc_info.value).lower()

    def test_only_first_six_visible_raises_error(self):
        """Test PAN with only first 6 visible raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("123456******")
        assert "last 4" in str(exc_info.value).lower()

    def test_only_last_four_visible_raises_error(self):
        """Test PAN with only last 4 visible raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("******1234")
        assert "first 6" in str(exc_info.value).lower()

    def test_too_few_visible_digits_raises_error(self):
        """Test PAN with too few visible digits raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("1234**56")
        assert "last 4" in str(exc_info.value).lower() or "first 6" in str(exc_info.value).lower()

    def test_too_many_visible_digits_raises_error(self):
        """Test PAN with too many visible digits raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("1234567890**1234")
        assert "too many" in str(exc_info.value).lower()

    def test_mask_character_not_asterisk_raises_error(self):
        """Test PAN masked with character other than asterisk raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("123456XXXXXX1234")
        assert "asterisk" in str(exc_info.value).lower()

    def test_empty_string_raises_error(self):
        """Test empty string raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("")
        assert "empty" in str(exc_info.value).lower()

    def test_non_digit_visible_chars_raises_error(self):
        """Test PAN with non-digit visible characters raises error."""
        with pytest.raises(MaskingError) as exc_info:
            validate_pan_masking("ABCD12******1234")
        assert "digit" in str(exc_info.value).lower() or "asterisk" in str(exc_info.value).lower()


class TestMaskingError:
    """Tests for MaskingError exception."""

    def test_masking_error_is_exception(self):
        """Test MaskingError is a valid exception."""
        error = MaskingError("Test error")
        assert isinstance(error, Exception)

    def test_masking_error_message(self):
        """Test MaskingError stores message."""
        error = MaskingError("Test error message")
        assert str(error) == "Test error message"
