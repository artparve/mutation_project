import pytest
from billing import bulk_discount

class TestBulkDiscount:
    """Тестирование функции расчёта скидки за объём"""

    @pytest.mark.parametrize("qty,expected", [
        (0, 0.0),         # Нет скидки при нуле
        (1, 0.0),         # Нет скидки при минимальном количестве
        (9, 0.0),         # Нет скидки ниже порога
        (10, 0.08),       # Граница на 10 — 8%
        (15, 0.08),       # Между 10 и 20 — 8%
        (19, 0.08),       # Граница перед 20 — 8%
        (20, 0.15),       # Граница на 20 — 15%
        (25, 0.15),       # Больше 20 — 15%
        (100, 0.15),      # Большие значения — 15%
    ])
    def test_bulk_discount(self, qty, expected):
        """Проверка всех пороговых значений скидки"""
        result = bulk_discount(qty)
        assert result == expected
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_qty", [-1, -10])
    def test_negative_qty(self, invalid_qty):
        """Проверка отрицательных значений (бизнес-логика: скидки нет)"""
        result = bulk_discount(invalid_qty)
        assert result == 0.0

    # def test_type_validation(self):
    #     """Проверка передачи нецелых типов"""
    #     with pytest.raises(TypeError):
    #         bulk_discount("10")
    #     with pytest.raises(TypeError):
    #         bulk_discount(None)
    #     with pytest.raises(TypeError):
    #         bulk_discount(10.5)
