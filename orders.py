"""Бизнес-логика заказов"""
"""Модуль для работы с заказами: создание, просмотр, редактирование и удаление."""

from typing import TypedDict, Set, List, Optional
from datetime import datetime

PRIORITIES = {"low", "med", "high"}


class Task(TypedDict):
    id_: int
    title: str
    amount: float
    email: str
    status: str
    tags: list[str]
    created_at: str
    due: Optional[str]
    closed_at: Optional[str]


# Глобальная переменная для хранения заказов
orders: List[Task] = []


def create_order(
    id_: int,
    title: str,
    amount: float,
    email: str,
    status: str,
    tags: set[str],
    created_at: str,
    due: Optional[str] = None,
    closed_at: Optional[str] = None
) -> dict:
    """
    Создаёт новый заказ.

    Args:
        id_: уникальный идентификатор заказа
        title: название заказа
        amount: сумма заказа
        email: email клиента
        status: статус заказа (new, in_progress, done, cancelled)
        tags: множество тегов
        created_at: дата и время создания (ISO 8601, UTC)
        due: дедлайн (ISO 8601 или None)
        closed_at: дата и время закрытия (ISO 8601 или None)

    Returns:
        dict: словарь с данными созданного заказа
    """
    # Проверяем, не существует ли заказ с таким ID
    if any(order['id_'] == id_ for order in orders):
        raise ValueError(f"Заказ с ID {id_} уже существует")

    # Валидация статуса
    valid_statuses = {"new", "in_progress", "done", "cancelled"}
    if status not in valid_statuses:
        raise ValueError(
            f"Недопустимый статус: {status}. Допустимые: {valid_statuses}")

    # Преобразуем множество тегов в список
    tags_list = list(tags)

    order: Task = {
        'id_': id_,
        'title': title,
        'amount': amount,
        'email': email,
        'status': status,
        'tags': tags_list,
        'created_at': created_at,
        'due': due,
        'closed_at': closed_at
    }

    orders.append(order)
    return order


def list_orders() -> List[Task]:
    """
    Возвращает список всех заказов.

    Returns:
        list: список словарей с данными заказов
    """
    return orders.copy()


def edit_order(order_id: int, **kwargs) -> bool:
    """
    Редактирует существующий заказ.

    Args:
        order_id: идентификатор заказа для редактирования
        **kwargs: поля для обновления (title, amount, status и т. д.)

    Returns:
        bool: True при успешном редактировании, False в случае ошибки
    """
    for order in orders:
        if order['id_'] == order_id:
            # Обновляем только переданные поля
            for key, value in kwargs.items():
                if key in order:
                    # Дополнительная валидация для статуса
                    if key == 'status':
                        valid_statuses = {
                            "new", "in_progress", "done", "cancelled"}
                        if value not in valid_statuses:
                            raise ValueError(
                                f"Недопустимый статус: {value}. Допустимые: {valid_statuses}")
            # Преобразуем теги в список, если это множество
                    if key == 'tags' and isinstance(value, set):
                        value = list(value)
                        order[key] = value
            return True
    return False


def remove_order(order_id: int) -> bool:
    """
    Удаляет заказ по идентификатору.

    Args:
        order_id: идентификатор удаляемого заказа

    Returns:
        bool: True при успешном удалении, False если заказ не найден
    """
    global orders
    initial_length = len(orders)
    orders = [order for order in orders if order['id_'] != order_id]
    return len(orders) < initial_length


# Пример использования
if __name__ == "__main__":
    # Создаём несколько заказов
    create_order(
        id_=1,
        title="Разработка веб‑сайта",
        amount=50000.0,
        email="client1@example.com",
        status="new",
        tags={"web", "frontend", "backend"},
        created_at="2024-09-17T10:00:00Z"
    )

    create_order(
        id_=2,
        title="Дизайн логотипа",
        amount=15000.0,
        email="client2@example.com",
        status="in_progress",
        tags={"design", "logo"},
        created_at="2024-09-16T14:30:00Z",
        due="2024-09-20T18:00:00Z"
    )

    # Выводим список заказов
    print("Все заказы:")
    for order in list_orders():
        print(order)

    # Редактируем заказ
    edit_order(1, status="in_progress", amount=55000.0)

    # Удаляем заказ
    remove_order(2)

    # Снова выводим список
    print("\nЗаказы после изменений:")
    for order in list_orders():
        print(order)
