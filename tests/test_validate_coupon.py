import pytest
from billing import validate_coupon

class TestValidateCoupon:
    """Тестирование функции проверки купона"""

    @pytest.mark.parametrize("code", [
        "SPORT10", "sport10", "SpOrT10",  # Разные регистры
        "NEWUSER5", "newuser5", "NEWuser5",
        "BLACKFRIDAY", "blackfriday", "BlackFriday"
    ])
    def test_valid_codes(self, code):
        """Проверка валидных купонов в разных регистрах"""
        assert validate_coupon(code) is True

    @pytest.mark.parametrize("code", [
        "SALE10", "VIP20", "INVALID", "12345", "", " ", None
    ])
    def test_invalid_codes(self, code):
        """Проверка невалидных и пустых купонов"""
        if code is None:
            # Функция ожидает строку, None должен вызвать ошибку
            with pytest.raises(AttributeError):
                validate_coupon(code)
        else:
            assert validate_coupon(code) is False

    def test_leading_trailing_spaces(self):
        """Проверка купонов с пробелами по краям"""
        assert validate_coupon(" SPORT10") is False
        assert validate_coupon("BLACKFRIDAY ") is False
        assert validate_coupon("  NEWUSER5  ") is False

    def test_numeric_and_special_characters(self):
        """Проверка купонов с числами и спецсимволами"""
        assert validate_coupon("SPORT10!") is False
        assert validate_coupon("NEWUSER5#") is False
        assert validate_coupon("BLACKFRIDAY2023") is False

    def test_type_errors(self):
        """Проверка передачи нестроковых типов"""
        with pytest.raises(AttributeError):
            validate_coupon(123)
        with pytest.raises(AttributeError):
            validate_coupon(['SPORT10'])
        with pytest.raises(AttributeError):
            validate_coupon(None)
