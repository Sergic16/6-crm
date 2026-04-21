import json
from typing import List, Dict, Any


def load() -> List[Dict[str, Any]]:
    """Загружает заказы из файла."""
    try:
        with open("orders.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Преобразуем теги в множества, если они сохранены как списки
            for order in data:
                if isinstance(order.get("tags"), list):
                    order["tags"] = set(order["tags"])
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("[WARN] Некорректный JSON в orders.json, создаём новый файл")
        return []


def save(orders: List[Dict[str, Any]]) -> None:
    """Сохраняет заказы в файл."""
    # Копируем данные и преобразуем множества в списки для JSON
    data_to_save = []
    for order in orders:
        order_copy = order.copy()
        if isinstance(order_copy.get("tags"), set):
            order_copy["tags"] = list(order_copy["tags"])
        data_to_save.append(order_copy)

    try:
        with open("orders.json", "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[ERROR] Ошибка сохранения: {e}")
