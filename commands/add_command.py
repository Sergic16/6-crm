from datetime import datetime


def setup_parser(subparsers):
    add_parser = subparsers.add_parser("add", help="Добавить новый заказ")
    add_parser.add_argument("--title", required=True,
                            type=str, help="Название заказа")
    add_parser.add_argument("--amount", required=True,
                            type=float, help="Сумма заказа")
    add_parser.add_argument("--email", required=True,
                            type=str, help="Email клиента")
    add_parser.add_argument("--due", type=str, help="Дедлайн (ISO 8601)")
    add_parser.add_argument("--tags", type=str, help="Теги через запятую")


def handle_add(manager, args):
    tags = set(args.tags.split(",")) if args.tags else set()
    try:
        order = manager.create_order(
            id=len(manager.list_orders()) + 1,  # Автогенерация ID
            title=args.title,
            amount=args.amount,
            email=args.email,
            status="new",
            tags=tags,
            created_at=datetime.now().isoformat(),
            due=args.due
        )
        print(f"Заказ {order['id']} успешно создан")
    except ValueError as e:
        print(f"[ERROR] {e}")
