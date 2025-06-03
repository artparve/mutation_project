import pytest

from billing import price_with_tax

class TestPriceWithTax:
    """Тестирование функции расчета цены с налогом"""
    
    @pytest.mark.parametrize("net,expected", [
        (100.0, 121.0),      # Базовый случай
        (0.0, 0.0),          # Нулевое значение
        (50.5, 61.11),        # Дробные числа
        (1e6, 1_210_000.0),  # Большие числа
    ])
    def test_positive_values(self, net, expected):
        """Проверка корректного расчета для неотрицательных значений"""
        result = price_with_tax(net)
        assert result == pytest.approx(expected, rel=1e-3), (
            f"Ожидалось {expected}, получено {result} для net={net}"
        )

    @pytest.mark.parametrize("negative_net", [
        -1.0,    # Отрицательное значение
        -100.0,  # Большое отрицательное значение
        -0.01,  # Граничное значение
        -1e6
    ])
    def test_negative_values_raises(self, negative_net):
        """Проверка вызова ValueError для отрицательных значений"""
        with pytest.raises(ValueError) as exc_info:
            price_with_tax(negative_net)
        
        assert str(exc_info.value) == "net must be non‑negative"

    def test_precision_rounding(self):
        """Проверка правильного округления"""
        assert price_with_tax(10.123) == pytest.approx(12.25, abs=0.005)
        assert price_with_tax(7.894) == pytest.approx(9.55, abs=0.005)