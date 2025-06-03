import pytest
from billing import cap_price

class TestCapPrice:
    """Тестирование функции ограничения цены сверху"""

    @pytest.mark.parametrize("price,cap,expected", [
        (100.0, 120.0, 100.0),     # Цена ниже лимита — не меняется
        (120.0, 120.0, 120.0),     # Цена равна лимиту
        (130.0, 120.0, 120.0),     # Цена выше лимита — ограничивается
        (0.0, 50.0, 0.0),          # Нулевая цена
        (50.0, 0.0, 0.0),          # Лимит нулевой
        (-10.0, 100.0, -10.0),     # Отрицательная цена ниже лимита
        (100.0, -10.0, -10.0),     # Лимит отрицательный — всегда лимит
        (-5.0, -10.0, -10.0),      # Оба значения отрицательные, цена выше лимита
        (-15.0, -10.0, -15.0),     # Оба значения отрицательные, цена ниже лимита
    ])
    def test_cap_price(self, price, cap, expected):
        """Проверка ограничения цены"""
        result = cap_price(price, cap)
        assert result == expected
        assert isinstance(result, float)

    def test_type_validation(self):
        """Проверка передачи нечисловых типов"""
        with pytest.raises(TypeError):
            cap_price("100.0", 120.0)
        with pytest.raises(TypeError):
            cap_price(100.0, "120.0")
        with pytest.raises(TypeError):
            cap_price(None, 120.0)
        with pytest.raises(TypeError):
            cap_price(100.0, None)
