import pytest
from billing import convert_currency, SUPPORTED_CURRENCIES

class TestConvertCurrency:
    """Тестирование функции конвертации валют"""

    @pytest.mark.parametrize("amount,currency,expected", [
        (100.0, "EUR", 100.0),      # Конвертация в ту же валюту
        (100.0, "USD", 108.70),     # 100 / 0.92 = 108.6956 → 108.70
        (50.0, "GBP", 43.48),       # 50 / 1.15 ≈ 43.478 → 43.48
        (0.01, "USD", 0.01),        # Минимальная сумма (0.01 / 0.92 ≈ 0.0109 → 0.01)
        (123.45, "GBP", 107.35)     # 123.45 / 1.15 ≈ 107.3478 → 107.35
    ])
    def test_supported_currencies(self, amount, currency, expected):
        """Проверка конвертации для поддерживаемых валют"""
        result = convert_currency(amount, currency)
        assert result == pytest.approx(expected, abs=0.001)
        assert isinstance(result, float)

    @pytest.mark.parametrize("currency", ["usd", "UsD", "gbP", "eur"])
    def test_case_insensitivity(self, currency):
        """Проверка нечувствительности к регистру валюты"""
        result = convert_currency(100.0, currency)
        assert result == convert_currency(100.0, currency.upper())

    @pytest.mark.parametrize("invalid_currency", ["JPY", "CAD", "RUB", ""])
    def test_unsupported_currencies(self, invalid_currency):
        """Проверка вызова KeyError для неподдерживаемых валют"""
        with pytest.raises(KeyError) as exc_info:
            convert_currency(100.0, invalid_currency)
        assert f"Unsupported currency {invalid_currency.upper()}" == exc_info.value.args[0]

    def test_zero_amount(self):
        """Проверка нулевой суммы"""
        assert convert_currency(0.0, "USD") == 0.0

    @pytest.mark.parametrize("amount", [-1.0, -100.0])
    def test_negative_amount(self, amount):
        """Проверка отрицательных сумм"""
        with pytest.raises(ValueError):
            convert_currency(amount, "USD")

    def test_precision_rounding(self):
        """Проверка правил округления"""
        # 10.0 / 0.92 = 10.869565 → 10.87
        assert convert_currency(10.0, "USD") == 10.87
        # 7.89 / 1.15 = 6.860869 → 6.86
        assert convert_currency(7.89, "GBP") == 6.86
