import pytest
from billing import tax_breakdown, TAX_RATE

class TestTaxBreakdown:
    """Тестирование функции разбиения суммы на нетто и налог"""

    @pytest.mark.parametrize("net", [
        0.0,
        1.0,
        100.0,
        99.99,
        1234.56,
        1e6,
        0.01,
    ])
    def test_basic_breakdown(self, net):
        """Проверка корректного разбиения и округления налога"""
        result = tax_breakdown(net)
        assert isinstance(result, tuple)
        assert len(result) == 2
        net_out, tax = result
        assert net_out == net
        expected_tax = round(net * TAX_RATE + 1e-8, 2)  # Стандартное округление
        assert tax == pytest.approx(expected_tax, abs=0.01)

    def test_negative_net(self):
        """Проверка работы с отрицательными значениями"""
        net = -100.0
        result = tax_breakdown(net)
        net_out, tax = result
        assert net_out == net
        expected_tax = round(net * TAX_RATE + 1e-8, 2)
        assert tax == pytest.approx(expected_tax, abs=0.01)

    def test_type_validation(self):
        """Проверка передачи нечисловых типов"""
        with pytest.raises(TypeError):
            tax_breakdown("100.0")
        with pytest.raises(TypeError):
            tax_breakdown(None)

    def test_return_type(self):
        """Проверка типа возвращаемого значения"""
        net = 50.0
        result = tax_breakdown(net)
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], float)
