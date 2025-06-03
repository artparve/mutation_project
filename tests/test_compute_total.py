import pytest
from billing import compute_total
from unittest.mock import patch

class TestComputeTotal:
    """Тестирование функции расчета итоговой стоимости с учетом налогов и купонов"""
    
    @pytest.mark.parametrize("price,qty,coupon,expected", [
        (100.0, 2, None, 243.21),         # Без купона
        (50.0, 3, "VIP20", 183.32),       # С купоном 20%
        (200.0, 1, "SALE10", 242.61),     # С купоном 10%
        (99.99, 5, "BLACKFRIDAY", 455.97) # Максимальная скидка
    ])
    def test_full_pipeline(self, price, qty, coupon, expected):
        """Интеграционный тест полного пайплайна расчетов"""
        result = compute_total(price, qty, coupon)
        assert result == pytest.approx(expected, abs=0.01)

    @pytest.mark.parametrize("qty", [0, -1, -5])
    def test_invalid_quantity(self, qty):
        """Проверка обработки невалидного количества"""
        with pytest.raises(ValueError) as exc_info:
            compute_total(100.0, qty, "SALE10")
        assert "qty must be positive" in str(exc_info.value)

    def test_rounding_behavior(self):
        with patch('billing.compute_subtotal', return_value=22.47), \
             patch('billing.booking_fee', return_value=5.0), \
             patch('billing.price_with_tax', return_value=32.96), \
             patch('billing.apply_coupon', return_value=29.0):
            
            result = compute_total(7.49, 3, "SALE10")
            assert result == 29.0
