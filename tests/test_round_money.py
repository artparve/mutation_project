import pytest
from decimal import Decimal, ROUND_HALF_UP
from billing import round_money

class TestRoundMoney:
    """Тестирование функции округления денежных значений"""

    @pytest.mark.parametrize("value,decimals,expected", [
        # Округление до 2 знаков (по умолчанию)
        (2.344, 2, 2.34),
        (2.345, 2, 2.35),
        (2.346, 2, 2.35),
        (2.335, 2, 2.34),  # Проверка ROUND_HALF_UP
        (-3.455, 2, -3.46),
        
        # Округление до 0 знаков (до целых)
        (2.4, 0, 2.0),
        (2.5, 0, 3.0),
        (-2.5, 0, -3.0),
        
        # Округление до 3 знаков
        (0.1234, 3, 0.123),
        (0.1235, 3, 0.124),
        
        # Округление до отрицательных знаков (до десятков, сотен)
        (123.45, -1, 120.0),
        (123.45, -2, 100.0),
        (-567.89, -1, -570.0),
        
        # Граничные значения
        (0.0, 2, 0.0),
        (999999.999999, 2, 1000000.0),
        (0.001, 2, 0.0),
        (0.001, 3, 0.001),
    ])
    def test_rounding_cases(self, value, decimals, expected):
        """Проверка различных сценариев округления"""
        result = round_money(value, decimals)
        assert result == pytest.approx(expected, abs=1e-9)
        assert isinstance(result, float)

    def test_default_decimals(self):
        """Проверка значения по умолчанию для decimals"""
        assert round_money(2.345) == 2.35
        assert round_money(3.1415) == 3.14

    @pytest.mark.parametrize("invalid_decimals", [2.5, "2", None])
    def test_invalid_decimals_type(self, invalid_decimals):
        """Проверка передачи нецелочисленных значений decimals"""
        with pytest.raises(TypeError):
            round_money(10.0, invalid_decimals)

    @pytest.mark.parametrize("value", ["10.5", None, [5.5]])
    def test_invalid_value_type(self, value):
        """Проверка передачи нечисловых типов для value"""
        with pytest.raises(TypeError):
            round_money(value)
