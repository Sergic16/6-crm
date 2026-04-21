def setup_parser(subparsers):
    tags_parser = subparsers.add_parser(
        "tags", help="Управление тегами заказа")
    tags_parser.add_argument("--id", required=True, type=str, help="ID заказа")
    tags_parser.add_argument(
        "--add", type=str, help="Добавить теги (через запятую)")
    tags_parser.add_argument("--remove", type=str,
                             help="Удалить теги (через запятую)")


def handle_tags(manager, args):
    order = next((o for o in manager.list_orders()
                 if o["id"] == args.id), None)
    if not order:
        print(f"[ERROR] Заказ {args.id} не найден")
        return
    current_tags = set(order["tags"])
    if args.add:
        current_tags.update(args.add.split(","))
    if args.remove:
        current_tags -= set(args.remove.split(","))
    manager.edit_order(args.id, tags=current_tags)
    print(f"Теги заказа {args.id} обновлены")
