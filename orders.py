from datetime import datetime
import uuid
import json
from typing import List, Dict, Any, Optional

# Список допустимых статусов заказов
VALID_STATUSES = {"new", "in_progress", "completed", "cancelled", "on_hold"}


class OrderManager:
    def __init__(self):
        """Инициализация менеджера заказов."""
        self._orders: List[Dict[str, Any]] = []

    def list_orders(self) -> List[Dict[str, Any]]:
        """Возвращает список всех заказов."""
        return self._orders

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Парсит строку даты в объект datetime.

        Args:
            date_str: строка даты в формате ISO 8601

        Returns:
            объект datetime

        Raises:
            ValueError: если формат даты некорректен
        """
        try:
            return datetime.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {date_str}")

    def create_order(
        self,
        title: str,
        amount: float,
        email: str,
        status: str = "new",
        tags: Optional[set] = None,
        due: Optional[str] = None
    ) -> Dict[str, Any]:
        """Создаёт новый заказ.

        Args:
            title: название заказа
            amount: сумма заказа
            email: email клиента
            status: статус заказа (по умолчанию "new")
            tags: теги заказа (по умолчанию пустой набор)
            due: дедлайн в формате ISO 8601 (опционально)

        Returns:
            созданный заказ как словарь

        Raises:
            ValueError: если статус недопустим
        """
        # Валидация статуса
        if status not in VALID_STATUSES:
            raise ValueError(
                f"Недопустимый статус: {status}. Доступные: {', '.join(VALID_STATUSES)}"
            )

        # Генерация уникального ID
        order_id = str(uuid.uuid4())

        order = {
            "id": order_id,
            "title": title,
            "amount": amount,
            "email": email,
            "status": status,
            "tags": tags or set(),
            "created_at": datetime.now().isoformat(),
            "due": due
        }

        self._orders.append(order)
        return order

    def remove_order(self, order_id: str) -> bool:
        """Удаляет заказ по ID.

        Args:
            order_id: ID заказа для удаления

        Returns:
            True, если заказ найден и удалён, иначе False
        """
        for i, order in enumerate(self._orders):
            if order["id"] == order_id:
                del self._orders[i]
                return True
        return False

    def edit_order(self, order_id: str, **kwargs) -> bool:
        """Редактирует существующий заказ.

        Args:
            order_id: ID заказа для редактирования
            **kwargs: поля для обновления

        Returns:
            True, если заказ найден и изменён, иначе False

        Raises:
            ValueError: если пытаются установить недопустимый статус
        """
        for order in self._orders:
            if order["id"] == order_id:
                # Валидация статуса при редактировании
                if "status" in kwargs:
                    if kwargs["status"] not in VALID_STATUSES:
                        raise ValueError(
                            f"Недопустимый статус: {kwargs['status']}. "
                            f"Доступные: {', '.join(VALID_STATUSES)}"
                        )
                # Обновление тегов — преобразуем строку в множество, если нужно
                if "tags" in kwargs and isinstance(kwargs["tags"], str):
                    kwargs["tags"] = set(kwargs["tags"].split(","))
                order.update(kwargs)
                return True
        return False

    def find_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Находит заказ по ID.

        Args:
            order_id: ID заказа

        Returns:
            заказ как словарь или None, если не найден
        """
        return next((o for o in self._orders if o["id"] == order_id), None)

    def get_overdue_orders(self) -> List[Dict[str, Any]]:
        """Возвращает просроченные заказы.

        Returns:
            список просроченных заказов
        """
        now = datetime.now()
        overdue = []
        for order in self._orders:
            if order["due"]:
                try:
                    due_date = self.parse_date(order["due"])
                    if due_date < now:
                        overdue.append(order)
                except ValueError:
                    # Пропускаем заказы с некорректным форматом даты
                    continue
        return overdue

    def filter_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Фильтрует заказы по тегу.

        Args:
            tag: тег для фильтрации

        Returns:
            список заказов с указанным тегом
        """
        return [o for o in self._orders if tag in o["tags"]]
