import pytest
from billing import compute_refund

class TestComputeRefund:
    """Тестирование функции расчёта возврата средств"""

    @pytest.mark.parametrize("total_paid,percentage,expected", [
        (100.0, 1.0, 100.0),      # Полный возврат
        (100.0, 0.0, 0.0),        # Нет возврата
        (200.0, 0.5, 100.0),      # 50% возврат
        (99.99, 0.25, 25.0),      # 25%, округление
        (123.45, 0.123, 15.18),   # Дробный процент, округление
        (0.0, 1.0, 0.0),          # Нулевая сумма
        (1.0, 0.3333, 0.33),      # Проверка округления вниз
    ])
    def test_valid_percentages(self, total_paid, percentage, expected):
        """Проверка корректного расчёта возврата для валидных процентов"""
        result = compute_refund(total_paid, percentage)
        assert result == pytest.approx(expected, abs=0.01)
        assert isinstance(result, float)

    @pytest.mark.parametrize("percentage", [-0.01, -1.0, 1.01, 2.0])
    def test_invalid_percentages(self, percentage):
        """Проверка вызова ValueError для невалидных процентов"""
        with pytest.raises(ValueError) as exc_info:
            compute_refund(100.0, percentage)
        assert "percentage 0..1" == str(exc_info.value)

    def test_type_validation(self):
        """Проверка передачи нечисловых типов"""
        with pytest.raises(TypeError):
            compute_refund("100.0", 0.5)
        with pytest.raises(TypeError):
            compute_refund(100.0, "0.5")
        with pytest.raises(TypeError):
            compute_refund(None, 0.5)
        with pytest.raises(TypeError):
            compute_refund(100.0, None)

    def test_rounding_behavior(self):
        """Проверка точности округления"""
        # 10.0 * 0.333 = 3.33 (округление)
        assert compute_refund(10.0, 0.333) == pytest.approx(3.33, abs=0.01)
        # 7.89 * 0.5 = 3.945 → 3.95
        assert compute_refund(7.89, 0.5) == pytest.approx(3.95, abs=0.01)

    def test_zero_total_paid(self):
        """Проверка возврата при нулевой оплаченной сумме"""
        assert compute_refund(0.0, 0.5) == 0.0
