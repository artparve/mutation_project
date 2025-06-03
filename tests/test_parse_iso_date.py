import pytest
from datetime import datetime
from billing import parse_iso_date

class TestParseIsoDate:
    """Тестирование функции разбора ISO-дат"""

    @pytest.mark.parametrize("date_str,expected", [
        ("2024-06-01", datetime(2024, 6, 1)),
        ("2025-12-31T23:59:59", datetime(2025, 12, 31, 23, 59, 59)),
        ("2000-01-01T00:00:00", datetime(2000, 1, 1, 0, 0, 0)),
        ("2023-03-15T12:30", datetime(2023, 3, 15, 12, 30)),
        ("2020-02-29T10:15:30.123456", datetime(2020, 2, 29, 10, 15, 30, 123456)),  # с микросекундами
    ])
    def test_valid_iso_dates(self, date_str, expected):
        """Проверка корректного разбора валидных ISO-дат"""
        result = parse_iso_date(date_str)
        assert result == expected
        assert isinstance(result, datetime)

    @pytest.mark.parametrize("invalid_str", [
        "2024/06/01",                # неверный формат
        "31-12-2025",                # неверный формат
        "2025-13-01",                # несуществующий месяц
        "2025-00-10",                # несуществующий месяц
        "2025-12-32",                # несуществующий день
        "2025-02-29",                # не високосный год
        "not-a-date",                # просто строка
        "",                          # пустая строка
        None,                        # None вместо строки
        123456,                      # число вместо строки
    ])
    def test_invalid_iso_dates(self, invalid_str):
        """Проверка вызова ValueError или TypeError для невалидных дат"""
        if isinstance(invalid_str, str):
            with pytest.raises(ValueError):
                parse_iso_date(invalid_str)
        else:
            with pytest.raises(TypeError):
                parse_iso_date(invalid_str)

    def test_timezone_support(self):
        """Проверка разбора строки с временной зоной"""
        # fromisoformat поддерживает "+HH:MM" и "-HH:MM"
        date_str = "2024-06-01T12:00:00+03:00"
        result = parse_iso_date(date_str)
        assert result.isoformat() == "2024-06-01T12:00:00+03:00"
        assert result.tzinfo is not None

    def test_leading_trailing_spaces(self):
        """Проверка обработки строк с пробелами по краям"""
        with pytest.raises(ValueError):
            parse_iso_date(" 2024-06-01 ")
