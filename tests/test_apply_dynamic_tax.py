import pytest
from billing import apply_dynamic_tax

class TestApplyDynamicTax:
    """Тестирование функции расчета цены с динамическим налогом"""

    @pytest.mark.parametrize("net,country,expected", [
        (100.0, "LV", 121.0),       # Латвия 21%
        (100.0, "lv", 121.0),       # Проверка нижнего регистра
        (100.0, "US", 120.0),       # Другая страна 20%
        (50.5, "LV", 61.11),        # Дробная сумма для LV (50.5 * 1.21)
        (50.5, "EE", 60.6),         # Дробная сумма для других (50.5 * 1.20)
        (0.0, "LV", 0.0),           # Нулевая сумма
        (1e6, "LV", 1_210_000.0),   # Большие числа
        (123.456, "GB", 148.15),    # Сложное округление (123.456*1.20=148.1472→148.15)
    ])
    def test_valid_cases(self, net, country, expected):
        """Проверка основных сценариев"""
        result = apply_dynamic_tax(net, country)
        assert result == pytest.approx(expected, abs=0.01)
        assert isinstance(result, float)

    @pytest.mark.parametrize("country", ["", "12", "LVA", "L"])
    def test_invalid_country_codes(self, country):
        """Проверка нестандартных кодов стран (все равно 20%)"""
        assert apply_dynamic_tax(100.0, country) == 120.0

    def test_case_insensitivity(self):
        """Проверка нечувствительности к регистру"""
        assert apply_dynamic_tax(100.0, "lV") == 121.0
        assert apply_dynamic_tax(100.0, "us") == 120.0

    @pytest.mark.parametrize("net", [-100.0, -0.01])
    def test_negative_net(self, net):
        """Проверка отрицательных сумм (допустимо по ТЗ?)"""
        assert apply_dynamic_tax(net, "LV") == pytest.approx(net * 1.21, abs=0.01)

    def test_type_validation(self):
        """Проверка обработки неверных типов данных"""
        with pytest.raises(TypeError):
            apply_dynamic_tax("100.0", "LV")
        with pytest.raises(AttributeError):  # country.upper() для нестрок вызовет AttributeError
            apply_dynamic_tax(100.0, None)
