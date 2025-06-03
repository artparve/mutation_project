import pytest
from datetime import datetime
from billing import is_weekend_rate

class TestIsWeekendRate:
    """Тестирование функции определения выходного дня"""

    @pytest.mark.parametrize("date_str,expected", [
        ("2024-06-03", False),  # Понедельник
        ("2024-06-04", False),  # Вторник
        ("2024-06-05", False),  # Среда
        ("2024-06-06", False),  # Четверг
        ("2024-06-07", False),  # Пятница
        ("2024-06-08", True),   # Суббота
        ("2024-06-09", True),   # Воскресенье
    ])
    def test_weekday_and_weekend(self, date_str, expected):
        """Проверка дней недели и выходных"""
        date = datetime.fromisoformat(date_str)
        assert is_weekend_rate(date) is expected

    def test_type_validation(self):
        """Проверка передачи не-дат"""
        with pytest.raises(AttributeError):
            is_weekend_rate("2024-06-08")
        with pytest.raises(AttributeError):
            is_weekend_rate(None)
        with pytest.raises(AttributeError):
            is_weekend_rate(12345)
