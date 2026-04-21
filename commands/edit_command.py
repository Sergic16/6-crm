def setup_parser(subparsers):
    edit_parser = subparsers.add_parser("edit", help="Редактировать заказ")
    edit_parser.add_argument("--id", required=True, type=str, help="ID заказа")
    edit_parser.add_argument("--title", type=str, help="Новое название")
    edit_parser.add_argument("--amount", type=float, help="Новая сумма")
    edit_parser.add_argument("--email", type=str, help="Новый email")
    edit_parser.add_argument(
        "--due", type=str, help="Новый дедлайн (ISO 8601)")


def handle_edit(manager, args):
    # Проверяем существование заказа
    order = manager.find_order(args.id)
    if not order:
        print(f"[ERROR] Заказ {args.id} не найден")
        return

    # Собираем поля для обновления
    update_fields = {}
    for field in ["title", "amount", "email", "due"]:
        value = getattr(args, field)
        if value is not None:
            update_fields[field] = value

    # Если нет полей для обновления
    if not update_fields:
        print("Не указаны поля для редактирования")
        return

    # Пытаемся обновить заказ
    try:
        if manager.edit_order(args.id, **update_fields):
            print(f"Заказ {args.id} успешно обновлён")
        else:
            print(f"[ERROR] Не удалось обновить заказ {args.id}")
    except ValueError as e:
        print(f"[ERROR] {e}")
