
from orders import VALID_STATUSES


def setup_parser(subparsers):
    status_parser = subparsers.add_parser(
        "status", help="Изменить статус заказа")
    status_parser.add_argument(
        "--id", required=True, type=str, help="ID заказа")
    status_parser.add_argument("status", type=str, choices=VALID_STATUSES,
                               help=f"Новый статус (доступные: {', '.join(VALID_STATUSES)})")


def handle_status(manager, args):
    # Проверяем существование заказа
    order = next((o for o in manager.list_orders()
                 if o["id"] == args.id), None)
    if not order:
        print(f"[ERROR] Заказ {args.id} не найден")
        return

    # Проверяем, что статус отличается от текущего
    if order["status"] == args.status:
        print(f"Заказ {args.id} уже имеет статус '{args.status}'")
        return

    # Пытаемся изменить статус
    if manager.edit_order(args.id, status=args.status):
        print(f"Статус заказа {args.id} изменён на '{args.status}'")
    else:
        print(f"[ERROR] Не удалось изменить статус заказа {args.id}")
