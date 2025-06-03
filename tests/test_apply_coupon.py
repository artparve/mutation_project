import pytest
from billing import apply_coupon, _round

class TestApplyCoupon:
    """Тестирование функции применения купонов"""
    
    @pytest.mark.parametrize("gross,coupon,expected", [
        (1000.0, "SPORT10", 900.0),      # Стандартная скидка 10%
        (500.0, "sport10", 450.0),       # Проверка нижнего регистра
        (200.0, "NEWUSER5", 190.0),      # Скидка 5%
        (1000.0, "BLACKFRIDAY", 750.0),  # Максимальная скидка
        (100.0, "invalid", 100.0),       # Неверный купон
        (50.0, "", 50.0),                # Пустая строка купона
        (200.0, None, 200.0),            # Отсутствие купона
    ])
    def test_coupon_application(self, gross, coupon, expected):
        """Проверка применения различных купонов"""
        result = apply_coupon(gross, coupon)
        assert result == pytest.approx(expected, abs=0.01), (
            f"Ожидалось {expected}, получено {result} для gross={gross}, coupon={coupon}"
        )

    @pytest.mark.parametrize("value", [
        123.456789,  # Высокая точность
        99.999,      # Граничное значение
        0.001,       # Минимальное значение
    ])
    def test_rounding_behavior(self, value):
        """Проверка округления до двух знаков"""
        result = apply_coupon(value, "SPORT10")
        expected = _round(value * 0.9)
        assert result == pytest.approx(expected, abs=0.005), (
            f"Некорректное округление: {value} -> {result} (ожидалось {expected})"
        )

    def test_zero_gross_handling(self):
        """Проверка обработки нулевой суммы"""
        assert apply_coupon(0.0, "BLACKFRIDAY") == 0.0
        assert apply_coupon(0.0, None) == 0.0

    def test_case_insensitivity(self):
        """Проверка нечувствительности к регистру купона"""
        assert apply_coupon(100, "sport10") == pytest.approx(90.0)
        assert apply_coupon(100, "SPORT10") == pytest.approx(90.0)
        assert apply_coupon(100, "Sport10") == pytest.approx(90.0)

    def test_return_type(self):
        """Проверка типа возвращаемого значения"""
        result = apply_coupon(100.0, "NEWUSER5")
        assert isinstance(result, float), "Функция должна возвращать float"