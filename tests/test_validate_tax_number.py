import pytest
from billing import validate_tax_number

class TestValidateTaxNumber:
    """Тестирование функции проверки налогового номера"""

    @pytest.mark.parametrize("tax_num", [
        "LV1234567891",   # Валидный номер (12 символов, начинается с LV)
        "LV0000000000",   # Валидный номер с нулями
        "LVABCDEFGIKL",  # Валидный формат, неважно, что буквы
    ])
    def test_valid_tax_numbers(self, tax_num):
        """Проверка валидных налоговых номеров"""
        assert validate_tax_number(tax_num) is True

    @pytest.mark.parametrize("tax_num", [
        "LT1234567891",     # Не LV
        "LV123456789",      # 11 символов
        "LV12345678902",    # 13 символов
        "123456789012",      # Нет префикса
        "",                  # Пустая строка
        "LV",                # Только префикс
        "LV123",             # Слишком коротко
        "lv12345678901",     # Маленькие буквы (чувствительно к регистру)
        "Lv12345678901",     # Смешанный регистр
        None,                # None вместо строки
        123456789012,        # Число вместо строки
    ])
    def test_invalid_tax_numbers(self, tax_num):
        """Проверка невалидных налоговых номеров"""
        if not isinstance(tax_num, str):
            with pytest.raises(AttributeError):
                validate_tax_number(tax_num)
        else:
            assert validate_tax_number(tax_num) is False

    def test_type_validation(self):
        """Проверка передачи нестроковых типов"""
        with pytest.raises(AttributeError):
            validate_tax_number(None)
        with pytest.raises(AttributeError):
            validate_tax_number(123456789012)
        with pytest.raises(AttributeError):
            validate_tax_number(["LV12345678901"])
