import pytest
from billing import compute_subtotal

class TestComputeSubtotal:
    """Тестирование функции расчета промежуточной суммы"""
    
    @pytest.mark.parametrize("price,qty,expected", [
        (100.0, 1, 100.0),      # Минимальное количество
        (50.5, 3, 151.5),       # Дробная цена
        (99.99, 10, 999.9),     # Граничные значения
        (0.01, 100, 1.0),       # Минимальная цена
        (2.505, 4, 10.02),      # Проверка округления вверх
        (1.2345, 5, 6.17)       # Округление до копеек
    ])
    def test_valid_cases(self, price, qty, expected):
        """Проверка корректного расчета для положительных значений"""
        result = compute_subtotal(price, qty)
        assert result == pytest.approx(expected, abs=0.005)
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_qty", [0, -1, -100])
    def test_non_positive_qty_raises(self, invalid_qty):
        """Проверка вызова ValueError для неположительного количества"""
        with pytest.raises(ValueError) as exc_info:
            compute_subtotal(100.0, invalid_qty)
        
        assert "qty must be positive" == str(exc_info.value)

    def test_precision_rounding(self):
        """Проверка правил округления"""
        # 2.505 * 4 = 10.02 (округляется вверх)
        assert compute_subtotal(2.505, 4) == pytest.approx(10.02, abs=0.001)
        # 7.499 * 3 = 22.497 → 22.50 (стандартное округление)
        assert compute_subtotal(7.499, 3) == pytest.approx(22.50, abs=0.001)

    def test_large_values(self):
        """Проверка работы с большими числами"""
        assert compute_subtotal(1_000_000.0, 100) == 100_000_000.0
        assert compute_subtotal(0.0001, 1_000_000) == pytest.approx(100.0)

    @pytest.mark.parametrize("invalid_type", ["5", None, [2]])
    def test_invalid_qty_type(self, invalid_type):
        """Проверка обработки неверных типов количества"""
        with pytest.raises(TypeError):
            compute_subtotal(100.0, invalid_type)
