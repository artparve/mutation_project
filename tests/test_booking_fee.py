import pytest
from billing import booking_fee

# def booking_fee(qty: int) -> float:
#     return _round(BOOKING_FEE_PER_TICKET * qty)

class TestBookingFee:
    """Тестирование функции расчета booking_fee"""

    BOOKING_FEE_PER_TICKET: float = 0.50
    
    @pytest.mark.parametrize("qty,expected", [
        (1, 0.5),      # Минимальное количество
        (3, 1.5),       # Дробная цена
        (99.99, 50),     # Граничные значения
        (0.01, 0.01),       # Минимальная цена
        (2.505, 1.25),      # Проверка округления вверх
        (1.2345, 0.62)       # Округление до копеек
    ])
    def test_valid_cases(self, qty, expected):
        result = booking_fee(qty)
        assert result == pytest.approx(expected, abs=0.005)
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_qty", [0, -1, -100])
    def test_non_positive_qty_raises(self, invalid_qty):
        """Проверка вызова ValueError для неположительного количества"""
        with pytest.raises(ValueError) as exc_info:
            booking_fee(invalid_qty)
        
        assert "qty must be positive" == str(exc_info.value)

    @pytest.mark.parametrize("invalid_type", ["5", None, [2]])
    def test_invalid_qty_type(self, invalid_type):
        """Проверка обработки неверных типов количества"""
        with pytest.raises(TypeError):
            booking_fee(invalid_type)