# Точка входа в приложение
"""
Основной файл приложения для учёта заказов.
Демонстрирует использование модулей orders и storage.
"""


import orders
import storage
from datetime import datetime, timezone
import uuid


def generate_unique_id() -> int:
    """Генерирует уникальный идентификатор заказа."""
    return abs(hash(uuid.uuid4())) % (10 ** 8)


if __name__ == "__main__":
    try:
        from datetime import timedelta
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Убедитесь, что файлы orders.py и storage.py находятся в той же директории.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
