from datetime import datetime


def setup_parser(subparsers):
    list_parser = subparsers.add_parser("list", help="Вывести таблицу заказов")
    list_parser.add_argument(
        "--overdue", action="store_true", help="Показать только просроченные заказы")
    list_parser.add_argument("--tag", type=str, help="Фильтр по тегу")
    list_parser.add_argument(
        "--limit", type=int, help="Ограничение количества записей")


def handle_list(manager, args):
    orders = manager.list_orders()

    # Фильтр по тегу
    if args.tag:
        orders = [o for o in orders if args.tag in o["tags"]]

    # Фильтр просроченных
    if args.overdue:
        now = datetime.now()
        orders = [
            o for o in orders
            if o["due"] and manager.parse_date(o["due"]) < now
        ]

    # Ограничение по количеству
    if args.limit:
        orders = orders[:args.limit]

    # Форматируем вывод
    if not orders:
        print("Список заказов пуст")
        return

    print("ID\tTitle\tAmount\tStatus\tDue")
    for order in orders:
        print(
            f"{order['id']}\t{order['title']}\t{order['amount']:.2f}\t{order['status']}\t{order['due'] or '—'}")
