import pytest
from billing import split_payment

class TestSplitPayment:
    """Тестирование функции разделения платежа на части"""

    @pytest.mark.parametrize("total,parts,expected", [
        (100.0, 4, [25.0, 25.0, 25.0, 25.0]),          # Идеальное деление
        (100.0, 3, [33.33, 33.33, 33.34]),             # Корректировка последней части
        (0.03, 3, [0.01, 0.01, 0.01]),                 # Минимальные значения
        (99.99, 1, [99.99]),                           # Одна часть
        (150.0, 5, [30.0, 30.0, 30.0, 30.0, 30.0]),    # Большое количество частей
        (123.45, 2, [61.73, 61.72]),                   # Нецелые суммы
        (0.0, 5, [0.0, 0.0, 0.0, 0.0, 0.0])           # Нулевая сумма
    ])
    def test_valid_split(self, total, parts, expected):
        """Проверка корректного разделения суммы"""
        result = split_payment(total, parts)
        assert result == pytest.approx(expected, abs=0.001)
        assert sum(result) == pytest.approx(total, abs=0.001)

    @pytest.mark.parametrize("invalid_parts", [0, -1, -5])
    def test_invalid_parts(self, invalid_parts):
        """Проверка вызова ошибки при невалидном количестве частей"""
        with pytest.raises(ValueError) as exc_info:
            split_payment(100.0, invalid_parts)
        assert "parts must be > 0" == str(exc_info.value)

    def test_rounding_consistency(self):
        """Проверка согласованности округлений"""
        # 10.01 / 3 = 3.336666... → [3.34, 3.34, 3.33] сумма 10.01
        assert split_payment(10.01, 3) == pytest.approx([3.34, 3.34, 3.33], abs=0.001)

    def test_last_part_adjustment(self):
        """Проверка корректировки последней части"""
        amounts = split_payment(100.01, 4)
        assert amounts[-1] == pytest.approx(25.01, abs=0.001)
        assert sum(amounts) == pytest.approx(100.01, abs=0.001)

    @pytest.mark.parametrize("parts", [1, 2, 5, 10])
    def test_output_length(self, parts):
        """Проверка количества возвращаемых частей"""
        result = split_payment(100.0, parts)
        assert len(result) == parts

    def test_type_validation(self):
        """Проверка обработки нечисловых типов"""
        with pytest.raises(TypeError):
            split_payment("100.0", 2)
        with pytest.raises(TypeError):
            split_payment(100.0, "2")
