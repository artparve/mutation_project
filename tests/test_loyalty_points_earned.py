import pytest
from billing import loyalty_points_earned, LOYALTY_POINT_RATE

class TestLoyaltyPointsEarned:
    """Тестирование функции начисления бонусных баллов"""

    @pytest.mark.parametrize("net,expected", [
        (0.0, 0),                # Нулевая сумма
        (1.0, 0),                # Меньше одного балла
        (50.0, 1),               # 50 * 0.02 = 1
        (99.99, 1),              # 99.99 * 0.02 = 1.9998 → 1
        (100.0, 2),              # 100 * 0.02 = 2
        (123.45, 2),             # 123.45 * 0.02 = 2.469 → 2
        (200.0, 4),              # 200 * 0.02 = 4
        (1e4, 200),              # Большое значение
        (-100.0, -2),            # Отрицательная сумма (логика допускает)
    ])
    def test_loyalty_points(self, net, expected):
        """Проверка начисления баллов для разных сумм"""
        result = loyalty_points_earned(net)
        assert result == expected
        assert isinstance(result, int)

    def test_fractional_points(self):
        """Проверка округления вниз при дробных баллах"""
        # 149.99 * 0.02 = 2.9998 → 2
        assert loyalty_points_earned(149.99) == 2

    def test_type_validation(self):
        """Проверка передачи нечисловых типов"""
        with pytest.raises(TypeError):
            loyalty_points_earned("100.0")
        with pytest.raises(TypeError):
            loyalty_points_earned(None)
        with pytest.raises(TypeError):
            loyalty_points_earned([100])

    def test_loyalty_point_rate_constant(self):
        """Проверка значения константы LOYALTY_POINT_RATE"""
        assert LOYALTY_POINT_RATE == 0.02
