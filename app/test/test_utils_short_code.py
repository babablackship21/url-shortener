import pytest
import string
from utils.short_code import generate_short_code

class TestGenerateShortCode:
    VALID_CHARS = set(string.ascii_letters + string.digits)

    def test_length(self):
        """Generated code should have the requested length."""
        for length in [1, 6, 10, 20]:
            code = generate_short_code(length)
            assert len(code) == length

    def test_characters(self):
        """Generated code should only contain valid characters."""
        for length in [6, 10, 20]:
            code = generate_short_code(length)
            assert set(code).issubset(self.VALID_CHARS)

    def test_invalid_length(self):
        """Invalid lengths should raise ValueError."""
        for length in [0, -1, True, 1.5, "6"]:
            with pytest.raises(ValueError):
                generate_short_code(length)

    def test_invalid_characters(self):
        """Generated code should not contain invalid characters."""
        code = generate_short_code(100)
        assert not any(c in code for c in string.punctuation + string.whitespace)
