"""Модуль для работы с хранилищем данных: загрузка и сохранение заказов."""

import json
from datetime import datetime
from typing import List, Dict, Optional

# Путь к файлу хранилища
path = "orders.json"

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Парсит строку даты в объект datetime.

    Args:
        date_str: строка даты в формате ISO 8601 или None

    Returns:
        datetime или None
    """
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except ValueError as e:
        print(f"[WARN] Некорректный формат даты: {date_str} — {e}")
        return None

def format_date(dt: Optional[datetime]) -> Optional[str]:
    """Форматирует объект datetime в строку ISO 8601.

    Args:
        dt: объект datetime или None

    Returns:
        строка в формате ISO 8601 или None
    """
    if not dt:
        return None
    return dt.isoformat()

def load() -> List[Dict]:
    """Загружает данные заказов из хранилища.

    Returns:
        list: список заказов (словарей) из хранилища
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        # Требование: если файла нет — вернуть []
        return []
    except json.JSONDecodeError as e:
        print(f"[WARN] Повреждённый JSON ({path}): {e}")
        return []

    orders: List[Dict] = []

    for item in raw.get("orders", []):
        try:
            order = {
                "id": int(item["id"]),
                "title": item["title"],
                "amount": float(item["amount"]),
                "email": item["email"],
                "status": item["status"],
                "tags": list(item.get("tags") or []),
                "created_at": parse_date(item["created_at"]) if item["created_at"] else None,
                "due": parse_date(item["due"]) if item["due"] else None,
                "closed_at": parse_date(item["closed_at"]) if item["closed_at"] else None
            }
            orders.append(order)
        except (KeyError, ValueError, TypeError) as e:
            print(f"[WARN] Пропущен заказ из-за ошибки данных: {e}")


    return orders

def save(orders: List[Dict]) -> None:
    """Сохраняет список заказов в хранилище.

    Args:
        orders: список заказов для сохранения
    """
    data = {
        "orders": [
            {
                "id": o["id"],
                "title": o["title"],
                "amount": o["amount"],
                "email": o["email"],
                "status": o["status"],
                "tags": o["tags"],
                "created_at": format_date(o["created_at"]) if o["created_at"] else None,
                "due": format_date(o["due"]) if o["due"] else None,
                "closed_at": format_date(o["closed_at"]) if o["closed_at"] else None
            }
            for o in orders
        ]
    }

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Данные успешно сохранены в {path}")
    except IOError as e:
        print(f"[ERROR] Не удалось сохранить файл {path}: {e}")
        raise
