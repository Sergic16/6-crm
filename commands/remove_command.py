def setup_parser(subparsers):
    remove_parser = subparsers.add_parser("remove", help="Удалить заказ по ID")
    remove_parser.add_argument(
        "--id", required=True, type=str, help="ID заказа")


def handle_remove(manager, args):
    if manager.remove_order(args.id):
        print(f"Заказ {args.id} удалён")
    else:
        print(f"[ERROR] Заказ {args.id} не найден")
