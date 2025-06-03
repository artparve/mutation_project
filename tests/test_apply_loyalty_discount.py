import pytest
from billing import apply_loyalty_discount

class TestApplyLoyaltyDiscount:
    """Тестирование функции применения скидки по бонусным баллам"""

    @pytest.mark.parametrize("gross,points,expected", [
        (10.0, 100, 9.0),       # 100 баллов → скидка 1.00
        (5.0, 50, 4.5),          # 50 баллов → 0.50
        (2.99, 299, 0.0),        # Скидка равна сумме → 0.0
        (3.0, 299, 0.01),        # 2.99 → 3.0 - 2.99 = 0.01
        (0.0, 100, 0.0),         # Нулевая сумма
        (10.0, 0, 10.0),         # Нет баллов
        (15.0, 123, 13.77),      # 123 балла → 1.23
        (1.0, 199, 0.0),         # Скидка больше суммы
    ])
    def test_valid_cases(self, gross, points, expected):
        """Проверка основных сценариев"""
        result = apply_loyalty_discount(gross, points)
        assert result == pytest.approx(expected, abs=0.001)
        assert isinstance(result, float)

    @pytest.mark.parametrize("points", [-100, -1])
    def test_negative_points(self, points):
        """Проверка отрицательных баллов (скидка становится надбавкой)"""
        assert apply_loyalty_discount(10.0, points) == pytest.approx(10.0 - (points * 0.01), abs=0.001)

    def test_rounding_behavior(self):
        """Проверка правил округления"""
        # 150 баллов → 1.50 скидка
        assert apply_loyalty_discount(10.0, 150) == 8.50
        # 149 баллов → 1.49 скидка
        assert apply_loyalty_discount(10.0, 149) == 8.51

    def test_type_validation(self):
        """Проверка обработки неверных типов данных"""
        with pytest.raises(TypeError):
            apply_loyalty_discount("10.0", 100)
        with pytest.raises(TypeError):
            apply_loyalty_discount(10.0, "100")
        with pytest.raises(TypeError):
            apply_loyalty_discount(None, 100)
